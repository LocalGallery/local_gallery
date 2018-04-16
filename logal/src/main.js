import Vue from 'vue';
import BootstrapVue from 'bootstrap-vue';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import "leaflet/dist/leaflet.css";

import L from 'leaflet';


import VueResource from 'vue-resource';
import Vue2Leaflet from 'vue2-leaflet';

import App from './App';
import store from './store';

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(VueResource);

Vue.component('v-map', Vue2Leaflet.Map);
Vue.component('v-tilelayer', Vue2Leaflet.TileLayer);
Vue.component('v-marker', Vue2Leaflet.Marker);

/* eslint-disable no-new */
new Vue({
    store,
    el: '#app',
    components: {App},
    template: '<App/>',
    created() {
        store.dispatch('requestPhotos');
        store.dispatch('requestLocations');
    },
});

delete L.Icon.Default.prototype._getIconUrl

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});
