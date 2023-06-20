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
