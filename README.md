# mimi
A simple secrets provision server

# Example

```shell
echo 'ほんとのきもちはひみつだよ' > secrets/example
ssh-keygen -t ed25519 -C 'Example SSH Key' -f example-key
nix run
curl -F "key=@example-key.pub" -X POST http://localhost:8111/get/example | rage --decrypt -i example-key
# ほんとのきもちはひみつだよ
```

NixOS configuration example:

```nix
{ pkgs, ... }: {
  systemd.services.mimi = {
    enable = true;
    description = "Update secrets";
    before = [ "network-online.target" ];
    serviceConfig = {
      Type = "oneshot";
      User = "root";
    };

    script = let
      bash = "${pkgs.bash}/bin/bash";
      curl = "${pkgs.curl}/bin/curl";
      hostname = "${pkgs.hostname}/bin/hostname";
      rage = "${pkgs.rage}/bin/rage";
      publicKey = "/etc/ssh/ssh_host_ed25519_key.pub";
      privateKey = "/etc/ssh/ssh_host_ed25519_key";
      mimiDomain = "mimi.example.com";
      descrypt = "${rage} --decrypt -i '${privateKey}'";
    in ''
      #!/bin/sh
      ${curl} -s -F "key=@${publicKey}" -X POST "https://${mimiDomain}/get/$(${hostname})" | {descrypt} | ${bash}
    '';
  };
}
```

# Todo

- Sign response content by the public key of the provisioner
- Encrypt the secrets on disk
- Access log
- IM notifications
