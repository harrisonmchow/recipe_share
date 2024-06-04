<template>
  <div ref="globe"></div>
</template>

<script>
import * as d3 from 'd3';
import * as topojson from 'topojson-client';
import worldData from '../assets/world-110m.json'; // Update the path accordingly

export default {
  props: {
    visitedCountries: {
      type: Array,
      required: true
    }
  },
  mounted() {
    this.createGlobe();
  },
  methods: {
    createGlobe() {
      const width = 950;
      const height = 500;
      let currentScale = 230; // Initial scale

      const projection = d3.geoOrthographic()
        .scale(currentScale)
        .translate([width / 2, height / 2])
        .clipAngle(90);

      const path = d3.geoPath()
        .projection(projection);

      const svg = d3.select(this.$refs.globe).append('svg')
        .attr('width', width)
        .attr('height', height);

      const graticule = d3.geoGraticule();

      svg.append('path')
        .datum(graticule)
        .attr('class', 'graticule')
        .attr('d', path);

      const world = topojson.feature(worldData, worldData.objects.countries).features;

      svg.selectAll('path.country')
        .data(world)
        .enter().append('path')
        .attr('class', 'country')
        .attr('d', path)
        .attr('fill', d => this.visitedCountries.includes(d.properties.name) ? 'green' : 'grey')
        .on('click', d => {
          console.log(d.srcElement["__data__"].properties.name);
          const countryName = d.srcElement["__data__"].properties.name
          if (countryName !== undefined && this.visitedCountries.includes(countryName)) {
            console.log(`taking you to ${countryName}`)
            window.location.href = `/travel/${countryName}`;
          }
        });

      const sphere = { type: 'Sphere' };
      svg.append('path')
        .datum(sphere)
        .attr('class', 'sphere')
        .attr('d', path);

      // Add drag functionality
      const drag = d3.drag()
        .subject(() => {
          const r = projection.rotate();
          return { x: r[0] / sens, y: -r[1] / sens };
        })
        .on('drag', (event) => {
          const rotate = projection.rotate();
          projection.rotate([event.x * sens, -event.y * sens, rotate[2]]);
          svg.selectAll('path').attr('d', path);
        });

      // Add zoom functionality
      const zoom = d3.zoom()
        .scaleExtent([1, 8]) // Define zoom scale limits
        .on('zoom', (event) => {
          currentScale = event.transform.k * 245;
          projection.scale(currentScale);
          svg.selectAll('path').attr('d', path);
        });

      const sens = 0.25; // Sensitivity for the dragging

      svg.call(drag);
      svg.call(zoom);

    },
    updateGlobe() {
      console.log("Updated");
      d3.select(this.$refs.globe)
      .selectAll('path.country')
      .attr('fill', d => this.visitedCountries.includes(d.properties.name) ? 'green' : 'grey')
    }
  },
  watch: {
    visitedCountries: function (newValue, oldValue) {
      this.updateGlobe();
    }
  }
};
</script>

<style>
.country {
  stroke: #000;
  stroke-width: 0.5px;
  cursor: pointer;
}

.graticule {
  fill: none;
  stroke: #777;
  stroke-width: 0.5px;
  stroke-opacity: 0.5;
}

.sphere {
  fill: none;
  stroke: #000;
  stroke-width: 1.5px;
}
</style>
