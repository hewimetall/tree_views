<template>
  <div class="p-12">
    <draggable
      :list="elems"
      item-key="pk"
      v-bind="dragOptions"
      :move="onMoveCallback"
      @start="move"
      @end="move"
    >
      <template #item="{ element }">
        <div class="container-fluid border m-2">
          <row :row="element" />
          <NestedItem v-if="element.tree_children" :elems="element.tree_children" />
          <NestedItem v-if="element.children" :elems="element.children" />
        </div>
      </template>
    </draggable>
  </div>
</template>

<script>
import draggable from 'vuedraggable';
import row from './row.vue';

export default {
  name: 'NestedItem',
  order: 16,
  components: {
    draggable, row,
  },
  computed: {
    dragOptions() {
      return {
        animation: 0,
        group: 'description',
        disabled: false,
        ghostClass: 'ghost',

      };
    },

    reversedMessage() {
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      this.$store.state.isEdit = !this.$store.state.isEdit;
      return 1;
    },
    edit: {
      get() { return this.$store.state.isEdit; },
      set(data) {
        this.$store.state.isEdit = data;
      },
    },
    myList: {
      get() {
        return this.elems;
      },
      set(value) {
        this.elems = value;
      },
    },

  },
  props:
  {
    elems: {
      required: true,
      type: Array,
    },
  },
  methods: {
    onMoveCallback(evt) {
      // console.log(evt.draggedContext); target
      // console.log(evt.relatedContext); to move
      this.target = evt.draggedContext.element;
      this.tomove = evt.relatedContext.element;
      // if (evt.draggedContext.element.type_obj) { return false; }
      return true;
    },

    save_data(el) {
      this.$store.state.isEdit = !this.$store.state.isEdit;
      console.log(el);
    },
    test_data: (el) => console.log(el, this),
    move() {
      this.$store.state.isEdit = !this.$store.state.isEdit;

      if (this.target === undefined || this.tomove === undefined) {
        return;
      }
      const targetPk = this.target.pk;
      const toPk = this.tomove.pk;

      this.$store.dispatch('moveTree', {
        target: targetPk,
        tomove: toPk,
      });
    },
  },
  data() {
    return {
      target: null,
      tomove: null,
    };
  },
};
</script>

<style scoped>
.content .row{
    padding: 8px;
}
</style>
