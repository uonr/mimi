{ lib, config, pkgs, ... }:
with lib;
let cfg = config.services.mimi;
in {
  options.services.mimi = {
    enable = mkEnableOption "Update secrets";
    id = mkOption {
      type = types.str;
      default = config.networking.hostName;
    };
    keyPath = mkOption {
      type = types.str;
      default = "/etc/ssh/ssh_host_ed25519_key";
    };
    publicKeyPath = mkOption {
      type = types.str;
      default = "/etc/ssh/ssh_host_ed25519_key.pub";
    };
    provisionerPublicKey = mkOption { type = types.str; };
    domain = mkOption { type = types.str; };
  };
  config = mkIf cfg.enable {
    systemd.services.mimi = {
      enable = true;
      description = "Update secrets";
      before = [ "network-online.target" ];
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {
        Type = "oneshot";
        User = "root";
      };
      environment = {
        NODE_ID = cfg.id;
        HOST_PUBLIC_KEY_PATH = cfg.publicKeyPath;
        HOST_KEY_PATH = cfg.keyPath;
        MIMI_DOMAIN = cfg.domain;
        PROVISIONER_PUBLIC_KEY =
          pkgs.writeText "key.pub" cfg.provisionerPublicKey;
      };
      script = let
        updateSecrets = pkgs.writeShellApplication {
          name = "update-mimi-secrets";

          runtimeInputs = with pkgs; [ curl rage gnutar xz gzip openssh ];

          text = builtins.readFile ./scripts/update-secrets.sh;
        };
      in "${pkgs.bash}/bin/bash ${updateSecrets}/bin/update-mimi-secrets";
    };
  };
}
