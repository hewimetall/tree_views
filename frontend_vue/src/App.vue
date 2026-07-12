<template>
<div class="container">
  <h1> Test nested set  </h1>
    <template v-for="(alert, index) in this.$store.state.alert" :key="index">
      <div v-if="alert.showDismissibleAlert" class="alert alert-danger alert-dismissible" role="alert">
        Dismissible Alert!
        <button
          type="button"
          class="btn-close"
          aria-label="Close"
          @click="alert.showDismissibleAlert = false"
        ></button>
      </div>
    </template>
  <div class="card">
    <div class="card-body">
      <div class="row m-2 d-flex">
        <button type="button" class="btn btn-primary" @click="add_struct">add struct</button>
      </div>
      <nested :elems="this.$store.state.elements" />
    </div>
  </div>
</div>
</template>

<script>
import nested from './components/nested.vue';

export default {
  name: 'App',
  components: {
    nested,
  },
  methods: {
    add_struct() {
      this.$store.dispatch('createNode',
        {
          type: 's',
          name: 'root',
        });
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
