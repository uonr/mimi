# mimi
A simple secrets provision server

# Example

```shell
echo 'ほんとのきもちはひみつだよ' > secrets/example
ssh-keygen -t ed25519 -C 'mimi' -f key
nix run 'github:uonr/mimi'
curl -F "key=@key.pub" -X POST http://localhost:8111/sign/example > example.sig
# -----BEGIN SSH SIGNATURE-----
# ...
# -----END SSH SIGNATURE-----
curl -F "key=@key.pub" -X POST http://localhost:8111/get/example | rage --decrypt -i key
# ほんとのきもちはひみつだよ

curl -F "key=@key.pub" -X POST http://localhost:8111/get/example | rage --decrypt -i key | ssh-keygen -Y check-novalidate -n file -f key.pub -s example.sig
# Good "file" signature with ED25519 key SHA256:...
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

- [x] Sign response content by the public key of the provisioner
- [ ] Encrypt the secrets on disk
- [ ] Access log
- [ ] IM notifications
