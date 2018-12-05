package co.upvest.contracts

import co.upvest.dry.essentials.bytes._
import co.upvest.dry.cryptoadt.secp256k1
import co.upvest.dry.cryptoadt.ethereum.ChainId
import co.upvest.dry.web3jz.{Web3jz, Config}
import co.upvest.dry.catz.syntax._

import cats.syntax.flatMap._
import cats.instances.try_._
import cats.instances.list._

import scala.concurrent.ExecutionContext
import scala.util.Success

object TestUtils {
  // mnemonic: text fall reveal replace bonus combine swap goat air bonus submit repair
  val pks: List[secp256k1.PrivateKey] = List(
    "e2ee547be17ac9f7777d4763c43fd726c0a2a6d40450c92de942d7925d620b6d",
    "0740fb09781e8fa771edcf1bddee93ad6772593b3139f1cf36b0d095d235887b",
    "ac72e464dac0448a28fa71b34bfe46b2356fe09bd4f5a73519ee60b3b92b9dab",
    "230eda6cc73da415d3b327426dde475a786bb5a0aeae2ca531aaaa8c0218a7a5",
    "91e3179925ef60e4d1f4daf0e7d67bdb5cf74ff3d456db0eb239e432290db31c",
    "66769c67a372926b945262a1c86b7944a669dbeab3d89771d7af691b3bfb20d8",
    "af40a15c4d369cdb39d01148d7b5f5dd4f9825447fabcbfc15e230db84fcb88b",
    "4ad882b7e0b24fd01ad6d2f281d469edb9d2bef2c2ee8871099c5fd7c7018317",
    "9042fc069b6abe8210d31195b382b61c3ee9149223fcb181016a49ba61a14d84",
    "bf32730f2b240c0c482126ecc1e2219554f3c738f19bd592e3ccf4cc005ddc1e"
  ) >>| { _.hex >>= secp256k1.PrivateKey.bigEndian } >>| { _.get  }

  val Success(web3jz) = Web3jz(
    Config(
      target = sys.env("GANACHE_TARGET"),
      chainId = ChainId(1337.toByte)
    )
  )(ExecutionContext.global)
}