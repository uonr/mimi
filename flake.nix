{
  description = "A simple secrets provision server";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";

    mach-nix.url = "github:davhau/mach-nix";
  };

  outputs = { self, nixpkgs, mach-nix, flake-utils, ... }:
    let pythonVersion = "python310";
    in flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        mach = mach-nix.lib.${system};

        pythonApp = mach.buildPythonApplication {
          python = pythonVersion;
          src = ./.;
          requirements = builtins.readFile ./requirements.txt;
          propagatedBuildInputs = with pkgs; [ rage ];
        };
        pythonAppEnv = mach.mkPython {
          python = pythonVersion;
          requirements = builtins.readFile ./requirements.txt;
        };
        pythonAppImage = pkgs.dockerTools.buildLayeredImage {
          name = pythonApp.pname;
          contents = [ pythonApp ];
          config.Cmd = [ "${pythonApp}/bin/main" ];
        };
      in rec {
        packages = {
          image = pythonAppImage;

          pythonPkg = pythonApp;
          default = packages.pythonPkg;
        };

        nixosModule = import ./nixos.nix;

        apps.default = {
          type = "app";
          program = "${packages.pythonPkg}/bin/main";
        };

        devShells.default = pkgs.mkShellNoCC {
          packages = [ pythonAppEnv ];
          propagatedBuildInputs = with pkgs; [ rage ];

          shellHook = ''
            export PYTHONPATH="${pythonAppEnv}/bin/python"
          '';
        };
      });
}
