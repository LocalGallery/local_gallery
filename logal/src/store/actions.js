import Vue from 'vue';

const PHOTOS_URL = '/api/1/photos/';
const LCOATIONS_URL = '/api/1/locations/';

export default {
    requestPhotos({commit}) {
        Vue.http.get(PHOTOS_URL).then(
            x => x.json(),
            x => console.error(x),
        ).then(x => commit("loadPhotos", x));
    },
    requestLocations({commit}) {
        Vue.http.get(LCOATIONS_URL).then(
            x => x.json(),
            x => console.error(x),
        ).then(x => commit("loadLocations", x));
    },
};
