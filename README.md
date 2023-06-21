# mimi
A simple secrets provision server

# Example

```shell
# Required for decrypting the secrets
nix-shell -p rage 

nix run 'github:uonr/mimi' init
# Set passphrase
mkdir -p secrets/example/
echo 'ほんとのきもちはひみつだよ' > secrets/example/secret
nix run 'github:uonr/mimi' serve
# Input passphrase
curl -F "key=@key.pub" -X POST http://localhost:8111/sign/example > example.sig
cat example.sig
# -----BEGIN SSH SIGNATURE-----
# ...
# -----END SSH SIGNATURE-----
curl -F "key=@key.pub" -X POST http://localhost:8111/get/example | rage --decrypt -i key > example.txt
cat example.txt
# ほんとのきもちはひみつだよ

ssh-keygen -Y check-novalidate -n file -f key.pub -s example.sig < example.txt
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
- [x] Passphrase
- [ ] Encrypt the secrets on disk
- [ ] Access log
- [ ] IM notifications
