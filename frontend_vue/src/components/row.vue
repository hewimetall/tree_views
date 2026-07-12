<template>
  <template v-if="row.type_obj === 'user'">
    <div v-if="edit" class="row p-2">
      <form class="input-group" @submit.prevent="save()">
        <input v-model="oldRow.fields.fullname" class="form-control" />
        <input v-model="oldRow.fields.email" class="form-control" />
        <input v-model="oldRow.fields.phone" class="form-control" />
        <input
          v-model="oldRow.fields.work"
          class="form-control"
          :list="oldRow.pk.split(':').join('_')"
        />
        <datalist :id="oldRow.pk.split(':').join('_')">
          <option v-for="item in selected" :key="item" :value="item"></option>
        </datalist>
        <button type="submit" class="btn btn-primary">Save</button>
        <button type="button" class="btn btn-secondary" @click="cansel()">Cansel</button>
      </form>
    </div>
    <div v-else class="row p-2">
      <div class="col">{{ row.fields.fullname }}</div>
      <div class="col">{{ row.fields.email }}</div>
      <div class="col">{{ row.fields.phone }}</div>
      <div class="col">{{ row.fields.work }}</div>
      <div class="col flex-grow-0">
        <div class="btn-group btn-group-sm">
          <button type="button" class="btn btn-warning" @click="editRow()">Edit</button>
          <button type="button" class="btn btn-info" @click="deleteRow()">Delete</button>
        </div>
      </div>
    </div>
  </template>
  <template v-else>
    <div v-if="edit" class="row p-2">
      <form class="input-group" @submit.prevent="save()">
        <input
          v-model="oldRow.fields.name"
          class="form-control"
          :placeholder="row.fields.fullname"
        />
        <button type="submit" class="btn btn-primary">Save</button>
        <button type="button" class="btn btn-secondary" @click="cansel()">Cansel</button>
      </form>
    </div>
    <div v-else class="row p-2">
      <div class="col">{{ row.fields.name }}</div>
      <div class="col flex-grow-0">
        <div class="btn-group btn-group-sm">
          <button type="button" class="btn btn-success" @click="new_user()">Add user</button>
          <button type="button" class="btn btn-success" @click="new_struct()">Add struct</button>
          <button type="button" class="btn btn-warning" @click="editRow()">Edit</button>
          <button type="button" class="btn btn-info" @click="deleteRow()">Delete</button>
        </div>
      </div>
    </div>
  </template>
</template>
<script>

export default {
  data() {
    return {
      oldRow: {},
      edit: false,
    };
  },
  computed: {
    selected: {
      get() {
        return this.$store.state.select;
      },
    },

  },
  props:
  {
    row: {
      required: false,
      type: Object,
    },
  },
  methods: {
    save() {
      this.$store.dispatch('changeNode', this.oldRow);
      this.edit = !this.edit;
      this.$store.state.isEdit = false;
    },
    new_user() {
      this.$store.dispatch('createNode',
        {
          type: 'u',
          username: this.row.pk,
          email: '',
          phone: '',
          parent: this.row.pk,
        });
    },

    new_struct() {
      this.$store.dispatch('createNode',
        {
          type: 's',
          name: this.row.pk,
          parent: this.row.pk,
        });
    },
    cansel() {
      this.edit = !this.edit;
      this.$store.state.isEdit = false;
    },
    editRow() {
      Object.assign(this.oldRow, this.row);
      this.$store.state.isEdit = true;
      this.edit = !this.edit;
    },
    deleteRow() {
      this.$store.dispatch('deleteTree', {
        dalete: true,
        target: this.row.pk,
      });
    },
  },
};
</script>
