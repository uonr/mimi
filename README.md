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
  services.mimi = {
    enable = true;
    provisionerPublicKey = ''
      ssh-ed25519 ... mimi
    '';
    domain = "mimi.example.com";
  };
}
```

# Todo

- [x] Sign response content by the public key of the provisioner
- [ ] Passphrase
- [ ] Encrypt the secrets on disk
- [ ] Access log
- [ ] IM notifications
