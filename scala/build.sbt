// *****************************************************************************
// Projects
// *****************************************************************************

lazy val root = (project in file("."))
  .settings(commonSettings: _*)
  .settings(
    libraryDependencies ++= Seq(
      library.dryWeb3jz % Test,
      library.scalaTest % Test,
    )
  )

lazy val library = new {
  object Version {
    val scalaTest = "3.0.5"
    val dry = "0.19.0-web3jz-SNAPSHOT"
  }

  val scalaTest = "org.scalatest" %% "scalatest" % Version.scalaTest
  val dryWeb3jz = "co.upvest" %% "dry-web3jz" % Version.dry
}

// *****************************************************************************
// Settings
// *****************************************************************************

lazy val commonSettings = Seq(
  scalaVersion := "2.12.7",
  organization := "co.upvest",
  scalacOptions ++= Seq(
    "-unchecked",
    "-deprecation",
    "-language:_",
    "-target:jvm-1.8",
    "-encoding", "UTF-8",
    "-Xfatal-warnings",
    "-Ywarn-unused-import",
    "-Yno-adapted-args",
    "-Ywarn-inaccessible",
    "-Ywarn-infer-any",
    "-Ywarn-nullary-override",
    "-Ywarn-nullary-unit",
    "-Ywarn-unused-import",
    "-Ypartial-unification",
    "-Xmacro-settings:materialize-derivations"
  ),
  scalacOptions in (Compile, console) ~= {
    _ filterNot (_ == "-Ywarn-unused-import")
  },
  javacOptions ++= Seq("-source", "1.8", "-target", "1.8"),
  cancelable in Global := true,
  fork in Global := true,
  resolvers += "Artifactory" at "http://artifacts.upvest.co/artifactory/sbt-dev/",
  resolvers += Resolver.mavenLocal,

  // This horse isn't amazing: https://github.com/sbt/sbt/issues/3519
  updateOptions := updateOptions.value.withGigahorse(false)
)
