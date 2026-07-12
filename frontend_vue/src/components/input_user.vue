<template>
  <form class="input-group">
    <input v-model="myfield.username" class="form-control" :placeholder="field.username" />
    <input v-model="myfield.email" class="form-control" :placeholder="field.email" />
    <input v-model="myfield.phone" class="form-control" :placeholder="field.phone" />
    <input
      v-model="myfield.work"
      class="form-control"
      :list="index"
      :placeholder="field.work"
    />
    <datalist v-if="field.select" :id="index">
      <option v-for="(select, i) in selected" :key="i" class="col-4" :value="select"></option>
    </datalist>
    <slot></slot>
  </form>
</template>

<script>
export default {
  data() {
    return {

      myfield: this.field,
    };
  },
  props: ['field', 'selected', 'index'],

};
</script>
