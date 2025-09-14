// Leer JSONs de raw_data y países
val rawDF = spark.read.json(args(0))
val countriesDF = spark.read.json(args(1))
val validCountries = countriesDF.select("name")

// Filtrar datos válidos
val filteredDF = rawDF.filter(col("value").isNotNull)
                      .join(validCountries, rawDF("country.value") === validCountries("name"))

val TYPE = args(2)
val OPTION = args(3)

val resultDF = TYPE match {
  case "country" => filteredDF.filter(col("country.value") === OPTION)
  case "date"    => filteredDF.filter(col("date") === OPTION)
}

resultDF.select(
    col("country.value").alias("COUNTRY"),
    col("date").alias("YEAR"),
    col("value").alias("VALUE")
).dropDuplicates()
 .sort(col("COUNTRY"), col("YEAR").desc)
 .coalesce(1)  // <<--- fuerza un solo archivo
 .write.mode("overwrite").json(args(4))

