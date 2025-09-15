// scala_processor/src/main/scala/DataProcessor.scala

import io.circe.generic.auto._
import io.circe.parser.decode
import scala.io.Source
import java.io.{File, PrintWriter}

// Usamos case classes para modelar la estructura del JSON de entrada.
// Esto nos da seguridad de tipos.
case class CountryInfo(id: String, value: String)
case class DataRecord(
    indicator: CountryInfo,
    country: CountryInfo,
    countryiso3code: String,
    date: String,
    value: Option[BigDecimal], // Usamos Option para manejar valores nulos (null)
    unit: String,
    obs_status: String,
    decimal: Int
)

object DataProcessor {

  def main(args: Array[String]): Unit = {
    if (args.length != 5) {
      println("Uso: java -jar <jar_file> <input_json> <country_list_txt> <output_csv> <filter_type> <filter_option>")
      sys.exit(1)
    }

    val inputJsonPath = args(0)
    val countryListPath = args(1)
    val outputPath = args(2)
    val filterType = args(3)
    val filterOption = args(4)

    // --- Lógica de get_countries_data ---

    // 1. Leer la lista de países permitidos
    val includedCountries = Source.fromFile(countryListPath).getLines.toSet

    // 2. Leer y parsear el archivo JSON de datos crudos
    val jsonString = Source.fromFile(inputJsonPath).getLines.mkString
    val decodedData = decode[List[DataRecord]](jsonString) match {
      case Right(data) => data
      case Left(error) =>
        println(s"Error al parsear el JSON: $error")
        sys.exit(1)
    }
    
    // 3. Filtrar por valor no nulo y por país en la lista
    val dataCountries = decodedData.filter(d =>
      d.value.isDefined && includedCountries.contains(d.country.value)
    )

    // --- Lógica de get_output_data ---

    // 4. Aplicar el filtro dinámico ('country' o 'date')
    val filteredData = filterType match {
      case "country" => dataCountries.filter(_.country.value == filterOption)
      case "date"    => dataCountries.filter(_.date == filterOption)
      case _         => List.empty[DataRecord] // Si el tipo es inválido, no retorna nada
    }

    // 5. Transformar a la estructura final, ordenar, y eliminar duplicados
    val result = filteredData
      .map(d => (d.country.value, d.date, d.value.get)) // Extraemos los valores
      .sortBy { case (country, year, _) => (country, -year.toInt) } // Ordenar por país ASC, año DESC
      .distinct

    // --- Escribir el resultado en un archivo CSV ---
    
    val writer = new PrintWriter(new File(outputPath))
    try {
      // Escribir la cabecera
      writer.println("COUNTRY,YEAR,VALUE")
      // Escribir cada fila
      result.foreach { case (country, year, value) =>
        writer.println(s"$country,$year,$value")
      }
    } finally {
      writer.close()
      println(s"Procesamiento con Scala completado. Resultado en: $outputPath")
    }
  }
}