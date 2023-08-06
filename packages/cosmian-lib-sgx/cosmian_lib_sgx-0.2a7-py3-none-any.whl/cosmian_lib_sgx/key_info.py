"""cosmian_lib_sgx.key_info module."""

from hashlib import sha3_256
from pathlib import Path

from cosmian_lib_sgx.crypto_lib import verify
from cosmian_lib_sgx.error import CryptoError


class KeyInfo:
    """KeyInfo class for participant key.

    Parameters
    ----------
    pubkey: bytes
        Bytes of an Ed25519 public key.
    enc_symkey: bytes
        Sealed symmetric key for the enclave.

    Attributes
    ----------
    pubkey: bytes
        Bytes of an Ed25519 public key.
    fingerprint: str
        Public key fingerprint as the 8 lowest bytes of SHA3-256(pubkey).
    enc_symkey: bytes
        Sealed symmetric key for the enclave.

    """

    def __init__(self, pubkey: bytes, enc_symkey: bytes):
        """Init constructor of KeyInfo."""
        self.pubkey: bytes = pubkey
        self.fingerprint: str = sha3_256(self.pubkey).digest()[-8:].hex()
        self.enc_symkey: bytes = enc_symkey

        sig, msg = self.enc_symkey[:64], self.enc_symkey[64:]
        assert len(sig) == 64
        assert len(msg) == 80
        # check Ed25519 signature of `enc_symkey`:
        # Sig(c, secretkey(pubkey)) || c = SealBox(symkey, enclave_pk)
        try:
            m = verify(msg, sig, self.pubkey)
            if m != msg:
                raise CryptoError(f"Expected message {msg.hex()}, found {m.hex()}")
        except CryptoError as exc:
            raise CryptoError(
                f"Failed to verify signature {sig.hex()} with pk {self.pubkey.hex()}"
            ) from exc


    @classmethod
    def from_path(cls, path: Path):
        """Extract KeyInfo from a path."""
        hexa: str
        # hexadecimal string of the public key
        hexa, *_ = path.stem.split(".")
        # hex string to bytes
        pubkey: bytes = bytes.fromhex(hexa)
        # read file content for the sealed symmetric key
        enc_symkey: bytes = path.read_bytes()

        return cls(pubkey, enc_symkey)
