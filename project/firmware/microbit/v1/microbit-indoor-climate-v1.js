basic.forever(function () {
    basic.showLeds(`
        . . . . .
        . # . # .
        . # # # .
        . . # . .
        . . . . .
        `)
    basic.showLeds(`
        # # . # #
        # # # # #
        # # # # #
        . # # # .
        . . # . .
        `)
    serial.writeLine("" + grove.readDataFromSCD30(grove.SCD30DataType.CO2) + ";" + grove.readDataFromSCD30(grove.SCD30DataType.Humidity) + ";" + grove.readDataFromSCD30(grove.SCD30DataType.Temperature) + ";" + grove.readDataFromSCD30(grove.SCD30DataType.CelsiusTemperature) + ";" + grove.readDataFromSCD30(grove.SCD30DataType.FarenheitTemperature))
    basic.pause(5000)
})