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

// https://inorganik.github.io/countUp.js/
import { CountUp } from 'countup.js';

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
                    color: ['#C6EBBE', '#00d400', '#38a64e']
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
        var isSmallScreen = window.innerWidth < 768;

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
                    axisLabel: {
                        fontSize: isSmallScreen ? 8 : 14 // Ajusta el tamaño de la fuente de los números en la escala del gauge
                    },
                    detail: {
                        valueAnimation: true,
                        offsetCenter: [0, '80%'],
                        formatter: function (value) {
                            return Math.round(value) + '%';
                        }
                    },
                    data: [
                        {
                            value: `${avanceFisico * 100}`,
                            name: 'Avance'
                        }
                    ]
                }
            ]
        };

        option && myChart.setOption(option);

        //  DIAS TRANSCURRIDOS
        let fechaInicio = new Date();
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

export function diasTranscurridos(progresoGral) {

    const contenedorAvanceDias = document.getElementById('avance-Dias');

    contenedorAvanceDias.innerHTML = '';
    
    if (progresoGral.length > 0) {

        const fechaInicial = new Date(progresoGral[0].fecha_inicio);
        
        let fechaFinal;

        let h2_div = document.createElement("h2");
        h2_div.classList.add("lg:text-lg", "text-base");

        let p_div = document.createElement("p");
        p_div.classList.add("lg:text-9xl", "text-7xl");
        p_div.setAttribute("id", "dias");

        if (progresoGral[0].fecha_final) {
            fechaFinal = new Date(progresoGral[0].fecha_final);
            h2_div.innerHTML = `Ejecución (Días)`;
        }
        else {
            fechaFinal = new Date();
            h2_div.innerHTML = `Días transcurridos`;
        }
        const diferenciaDias = (fechaFinal - fechaInicial) / (1000 * 60 * 60 * 24);
        let diasTranscurridos = Math.round(diferenciaDias);
        diasTranscurridos = diasTranscurridos.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");

        contenedorAvanceDias.appendChild(h2_div);
        contenedorAvanceDias.appendChild(p_div);
        
        let dias = new CountUp('dias', diasTranscurridos, {duration: 2, startVal: 0});
        if (!dias.error) {
            dias.start();
        } else {
            console.error(dias.error);
        }       
    }
}