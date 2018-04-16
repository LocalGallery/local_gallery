<template>
    <b-tabs>
        <b-tab title="Photos" active>
            <photos @set-item="photoClicked"></photos>
        </b-tab>
        <b-tab title="Places">
            <locations @set-item="locationClicked"></locations>
        </b-tab>
        <b-tab title="People" disabled>
            <br>Disabled tab!
        </b-tab>
    </b-tabs>
</template>

<script>
    import bTabs from 'bootstrap-vue/es/components/tabs/tabs';
    import store from '../store';
    import Photos from './Photos';
    import Locations from './Locations';

    export default {
        store,
        data() {
            return {};
        },
        components: {
            Locations,
            Photos,
            bTabs,
        },
        methods: {
            photoClicked(item) {
                // console.log('PRIMARY', item);
                this.$emit('set-item', item);
            },
            locationClicked(item) {
                // console.log('PRIMARY', item);
                this.$emit('set-item', item);
            },
        },
    };
</script>

<style scoped>
</style>
