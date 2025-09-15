// scala_processor/build.sbt

ThisBuild / version := "0.1.0-SNAPSHOT"
ThisBuild / scalaVersion := "2.13.10" // o la versión que tengas instalada

lazy val root = (project in file("."))
  .settings(
    name := "ScalaDataProcessor"
  )

// Dependencia para parsear JSON con Circe
libraryDependencies ++= Seq(
  "io.circe" %% "circe-core"    % "0.14.3",
  "io.circe" %% "circe-generic" % "0.14.3",
  "io.circe" %% "circe-parser"  % "0.14.3"
)