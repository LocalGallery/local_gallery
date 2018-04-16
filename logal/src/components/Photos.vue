<template>
    <b-table striped hover :items="photos" :fields="fields"
             @row-clicked="setItem">
        <template slot="checkbox" slot-scope="data">
            <b-checkbox></b-checkbox>
        </template>
        <template slot="photo_file" slot-scope="data">
            <img :src="data.value" height="50">
        </template>
    </b-table>
</template>

<script>
    import bTable from 'bootstrap-vue/es/components/table/table';
    import store from '../store';
    // import bCheckbox from 'bootstrap-vue/es/components/form-checkbox/form-checkbox';

    const fields = [
        'checkbox',
        'id',
        'name',
        'location_id',
        'photo_file',
    ];

    export default {
        store,
        computed: {
            photos() {
                return this.$store.state.photos;
            },
        },
        data() {
            return {
                fields,
            };
        },
        components: {
            bTable,
        },
        methods: {
            setItem(row) {
                // console.log('PHOTOS', row);
                this.$emit('set-item', row);
            },
        },
    };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    /*h1, h2 {*/
    /*font-weight: normal;*/
    /*}*/

    /*ul {*/
    /*list-style-type: none;*/
    /*padding: 0;*/
    /*}*/

    /*li {*/
    /*display: inline-block;*/
    /*margin: 0 10px;*/
    /*}*/

    /*a {*/
    /*color: #42b983;*/
    /*}*/
</style>
