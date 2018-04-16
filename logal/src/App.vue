<template>
    <div id="app">
        <div class="container-fluid">
            <h1>Local Gallery!!!!!</h1>
            <div class="row">
                <div class="col-sm-8">
                    <primary-panel @set-item="setItem"></primary-panel>
                </div>
                <div class="col-sm-4">
                    <detail-panel :item="currentItem"></detail-panel>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import PrimaryPanel from './components/PrimaryPanel';
    import DetailPanel from './components/DetailPanel';

    export default {
        name: 'App',
        data() {
            return {
                currentItem: null,
            };
        },
        components: {
            PrimaryPanel,
            DetailPanel,
        },
        methods: {
            setItem(item) {
                // console.log("APP", item);
                this.currentItem = item;
            },
        },
    };
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }
</style>
