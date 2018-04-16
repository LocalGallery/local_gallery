import Vue from 'vue';

const PHOTOS_URL = '/api/1/photos/';
const LOCATIONS_URL = '/api/1/locations/';

export default {
    loadPhotos(state, data) {
        state.photos = data;
    },
    loadLocations(state, data) {
        state.locations = data;
    },
    allLoaded() {
        state.loaded = true;
    },
};
