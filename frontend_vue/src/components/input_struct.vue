<template>
  <form class="input-group">
    <input v-model="myfield.label" class="form-control" :placeholder="fields.username" />
  <slot></slot>
  </form>
</template>

<script>
export default {
  data() {
    const index = Math.random();
    return { index, myfield: this.fields };
  },
  props:
  {
    fields: {
      required: false,
      type: Object,
    },
  },

};
</script>
