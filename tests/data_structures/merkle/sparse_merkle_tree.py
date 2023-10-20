import random

from avlgo.data_structures.merkle import SparseMerkleTree
from avlgo.data_structures.utils import Direction
from avlgo.profiler import TimeContext, object_memory_dword


def test_mark():
    smt = SparseMerkleTree()
    nodes = [
        b'c866eb02a1d9f1bf1f1d04e8aad605c4620c0f7c54bf01bec2478edeeb1d9a1c',
        b'e83ad8977e8fc0eebffcf928e7faf1f36ee3eb74af8bb7af273ca7a97dc045cf',
        b'e76e4229cd2dce255be023b60bbafedaf2b94f39a02098949252534ad6afd079',
        b'a64021fdbeb8f198f80543a9ea2c194361f88ff033ebbbba06af39a7deb48434',
        b'227f89f30d59e0b77270339d64e788fd44d611581728e09ec76df78aa1593fbd',
        b'ab819b6e6b80d0ef3a7dfc635757c1714df75e780842436f82989ed31679c700',
        b'3f88ab14d3fe81e5dd98c4d6866b7eb73549f066a3881f99b8955e0ae1289247',
        b'077a47a150ad3834a95d55f7a40f7d6b43c07e597f36edaaf92d8d7560a96056',
        b'd031377eea4f5d808e1c1a93f823804dccb4f1b3c95b2fb9cb4c1b6139391a38',
        b'32761ea95a6df424cd53d6393ea00fabf8bdd626827ccfcac8c8358b0dc87b5a',
        b'6657da1a53d4134a210305e6bcef4299f0b6a973bc7e5d355cd8fa012f0f8e64',
        b'4560042e2633a5b516b3c0acfcd248c7bfdf29c97c9fc3c6d600a4c770b3056c',
        b'10219ae35726df32aa6d1818389105eee55892d899c6b821a0e982e418661061',
        b'532cae056cebfcc2f4c69f25df75f0e7544c986b191f3eb753f6949e5df39f7f',
        b'9eca8158a1a3b0a003f06ac88e9fc07a543ba28b0173e508cc53a23ebe3d1a02',
        b'2e72045f979262df0e978bdb9238ad59c8b8c8ab1d0907af12508633085fc425',
        b'68b838d8afead35de50654f914944596b2f4e5d8b77337aef4f5a4c2154a39e1',
        b'51ca75b5b2137980995985aa083d415d097fca9c35dc2521e6ea4df19742127e',
        b'c611b6d7090afb060cd3b94fe81c6a2f36da52a4f55f0fa211912d6412f5f71f',
        b'87492c7f706630dffd50071e8a1864c0e904999bd1127a30c86f25403caa99db'
    ]

    for node in nodes:
        smt.mark(node)
        assert smt.is_marked(node)

    for node in nodes:
        assert smt.is_marked(node)


def test_proof():
    smt = SparseMerkleTree()
    data = b'aaaaa1935592c563da9a769cd9c194a78fb854b825bffa13aa1146c6ac0baaaa'

    proof = smt.proof(data)
    assert proof.hashes == []
    assert proof.directions == []

    smt.mark(data)
    proof = smt.proof(data)
    assert proof.directions[2] == Direction.RIGHT
    assert proof.hashes[2] == b'7437365578b682de87174ba8a7f5eaa30ee982b7d8e9e3c6e86d263518ffc493'


def test_validate():
    smt = SparseMerkleTree()
    nodes = [
        b'fc96a1935592c563da9a769cd9c194a78fb854b825bffa13aa1146c6ac0b9c36',
        b'c61c39651550c6118b535b66f5e87225707f45573461ae62023456fdfca348e7',
        b'b74248184be42b3054f96abd49980f59c404b28a05a78751a4eb1fbc2207ce12',
        b'8613cb37bfd4d34f1be89e53b8ca8a642ad2ddccfda27af4a121f36c4db15dcb',
        b'a7624f3b1da69676e649165fa1f10f86e9a11fd30cbbdc8065a5844cdc462248',
        b'67ecd1eca18f5047680b43b4f163ed1be64bed73d630ad7d753687f3cbdf4ff9',
        b'56c0a84861b547903d7f90c2e1c5a8d4f574e66d930d3ee7b3a631d014f955e4',
        b'c9a2cad624d6882093d2e232111d50dc8eb63a67370348222d14dee44c2bef98',
        b'c908ae8eee03b13fe2f5b452ed4f0224edcf610a7e51db7047bd0aa9216e1b65',
        b'89e26a7fb6572b16100d9689eaff6baa6a891dd3feed35620193e10b36ff6ad4',
        b'7ac258675b989a975937bf2a9c1f6a99bf0e0c33b305d86a87340a5883715de0',
        b'd9708e802584e177d47491bca0a1de802b8941e131a544d6e8af368577cf16eb',
        b'f658abffec9c9d20a10540d39481608a949186390404f3a70ef1b6b8f3b88f76',
        b'91849e50ec07412b03672c29a65b248becdded5ef6ff302b547924b821238478',
        b'3242c577fb0f487c4545c69a45100a594d9cdda2bed024e9416ac3bc872b7b46',
        b'b64b3e6429204b17fc692c0c609ff61d528d99f9c85d22fb5c4611503f547354',
        b'ac898996c0acce2a1315b30af4d82f67c0dcfd4f488e65586b17410ff92fea44',
        b'7f65869812d249e98d706309c3ad4f74c9e0d566fbfb5361efa0c150cbb8b3be',
        b'2ee8ed1b9fefd4786b342e48af0f43fd2f5baf9bbd21c7c5f2b7d8f861fa299c',
        b'91c2bc7776909f2d405f7d2423eee9eace0ceaf98b9dec1f4d681adbb273a808'
    ]

    for node in nodes:
        smt.mark(node)
        assert smt.validate(smt.tree_digest, True, smt.proof(node)) is True
        assert smt.validate(smt.tree_digest, False, smt.proof(node)) is False

    for node in nodes:
        assert smt.validate(smt.tree_digest, True, smt.proof(node)) is True
        assert smt.validate(smt.tree_digest, False, smt.proof(node)) is False


def test_time():
    smt = SparseMerkleTree()
    timer = TimeContext()

    with timer:
        for _ in range(10**3):
            node = random.randbytes(32).hex().encode()
            smt.mark(node)
            assert smt.is_marked(node)

    assert timer.time.total_seconds() < 4


def test_space():
    smt = SparseMerkleTree()

    for _ in range(10 ** 3):
        node = random.randbytes(32).hex().encode()
        smt.mark(node)

    assert object_memory_dword(smt) < 700000
