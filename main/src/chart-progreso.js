import * as echarts from 'echarts/core';
import {
    DatasetComponent,
    GridComponent,
    VisualMapComponent,
    TooltipComponent
} from 'echarts/components';
import {
    BarChart,
    GaugeChart
} from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';

export function chartProgreso(actividades) {

    const chartBarras = document.getElementById('barras-Chart');
    const chartGauge = document.getElementById('avance-Chart');


    if (actividades) {

        chartBarras.style.height = `${1.4 * actividades.length + 8}rem`;

        // Calcular la suma total de las ponderaciones
        const totalPonderacion = actividades.reduce((sum, actividad) => sum + actividad.ponderacion, 0);


        const avanceFisico = actividades.reduce((sum, actividad) => sum + (actividad.avance / totalPonderacion * actividad.ponderacion / 100), 0);

        const resultado = actividades.map(actividad => [
            ((actividad.ponderacion / totalPonderacion) * 100).toFixed(1), // Ponderación real en porcentaje y redondeado a un decimal
            actividad.avance, // Avance
            actividad.actividad // Nombre de la actividad
        ]);

        // Para encontrar el máximo valor de la ponderación porcentual
        const maxPonderacion = resultado.reduce((max, current) => {
            return Math.max(max, parseFloat(current[0])); // Comparar el valor máximo actual con el primer elemento de cada sub-arreglo
        }, 0); // Inicializar max en 0

        const resultadoChart = resultado.reverse();

        // Insertar la cabecera al inicio del array resultado
        resultadoChart.unshift(['score', 'avance', 'actividad']);

        // ECHARTS BARRAS
        // para las columnas la formula rem es y=1.4x+8
        echarts.use([
            DatasetComponent,
            GridComponent,
            VisualMapComponent,
            BarChart,
            CanvasRenderer
        ]);

        var myChart = echarts.init(chartBarras);
        var option;

        option = {
            dataset: {
                source: resultadoChart
            },
            grid: { containLabel: true },
            xAxis: {
                type: 'value',  // Cambiado de 'name' a 'value' para un eje numérico
                name: 'Avance (%)',
                min: 0,          // Establece el valor mínimo del eje X
                max: 100,        // Establece el valor máximo del eje X
            },
            yAxis: { type: 'category' },
            visualMap: {
                orient: 'horizontal',
                left: 'center',
                min: 0,
                max: maxPonderacion,
                text: ['Max', 'Ponderacion | Min'],
                dimension: 0,
                inRange: {
                    color: ['#65B581', '#FFCE34', '#FD665F']
                }
            },
            series: [
                {
                    type: 'bar',
                    encode: {
                        x: 'avance',
                        y: 'actividad'
                    },
                }
            ]
        };

        option && myChart.setOption(option);

        // ECHARTS GAUGE
        // https://echarts.apache.org/examples/en/editor.html?c=gauge-simple

        echarts.use([TooltipComponent, GaugeChart, CanvasRenderer]);

        var myChart = echarts.init(chartGauge);
        var option;

        option = {
            tooltip: {
                formatter: '{a} <br/>{b} : {c}%'
            },
            series: [
                {
                    name: '(%)',
                    type: 'gauge',
                    progress: {
                        show: true,
                        itemStyle: {
                            color: '#00d400' // Cambia el color del progreso a verde
                        }
                    },
                    pointer: {
                        itemStyle: {
                            color: '#00d400' // Cambia el color del puntero a verde
                        }
                    },
                    detail: {
                        valueAnimation: true,
                        formatter: function (value) {
                            return Math.round(value); // Redondea el valor a un entero
                        }
                    },
                    data: [
                        {
                            value: avanceFisico * 100,
                            name: 'Avance'
                        }
                    ]
                }
            ]
        };

        option && myChart.setOption(option);

    }

    else {
        chartBarras.innerHTML = '';
        // Elimina el atributo _echarts_instance_
        chartBarras.removeAttribute('_echarts_instance_');
        // Elimina el atributo style
        chartBarras.removeAttribute('style');

        chartGauge.innerHTML = '';
        chartGauge.removeAttribute('_echarts_instance_');
        chartGauge.removeAttribute('style');
    }

}

