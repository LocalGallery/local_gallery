<template>
    <b-card>
        <div v-if="item">
            <img :src="item.photo_file" class="img-fluid">
            <p>
                {{ item.name }}
            </p>
        </div>
        <p v-else>Choose an image.</p>
        <div v-if="item && item.coords" style="height: 500px;width:100%">
            <v-map :zoom=13 :center="item.coords">
                <v-tilelayer
                    url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"></v-tilelayer>
                <v-marker :lat-lng="item.coords"></v-marker>
            </v-map>
        </div>
    </b-card>
</template>

<script>
    import bCard from 'bootstrap-vue/es/components/card/card';
    import bButton from 'bootstrap-vue/es/components/button/button';
    import store from '../store';

    export default {
        store,
        components: {
            bCard,
            bButton,
        },
        props: [
            'item',
        ],
        data() {
            return {
                // item,
            };
        },
        methods: {},
    };
</script>

<style scoped>
</style>
