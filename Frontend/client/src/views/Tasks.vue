<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h1>Tasks</h1>
        <hr><br>
        <div class="row">
          <b-form inline id="addTaskId" class="card-text col">
            <label class="mr-sm-2">Task ID:</label>
            <b-input id="addTaskIdForm"
                     type="text"
                     v-model="addTaskIdForm"
                     class="mb-2 mr-sm-2 mb-sm-0"
            >id</b-input>
            <b-button type="default" @click.prevent="submitId" variant="primary">
              Submit</b-button>
          </b-form>
          <button type="button" class="btn btn-success btn-sm col"
                  @click.prevent="refreshAllTasks">
            Refresh tasks
          </button>
        </div>
        <br><br>
        <table class="table table-hover" id="tasks-table">
          <thead>
            <tr>
              <th scope="col">Time</th>
              <th scope="col">ID</th>
              <th scope="col">Type</th>
              <th scope="col">State</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(task, index) in tasks" :key="task.task_id">
              <td class="align-middle">{{task.time}}</td>
              <td class="align-middle">{{task.task_id}}</td>
              <td class="align-middle">{{task.type}}</td>
              <td class="align-middle">{{task.state}}</td>
              <td class="align-middle">
                <div class="btn-group" role="group">
                  <button v-if="isTaskFailed(index)"
                          type="button" class="btn btn-success btn-sm"
                          :disabled="!isTaskDone(index)">
                    <span class="spinner-border spinner-border-sm pb-2" role="status"
                          aria-hidden="true"
                          v-if="!isTaskDone(index)">
                    </span>
                    <span v-else class="align-middle" @click.prevent="download(index)">
                      Download
                    </span>
                  </button>
                  <button type="button" class="btn btn-danger btn-sm" @click="removeTask(index)">
                    Remove
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style>
#tasks-table {
  text-align: center;
}
</style>

<script>
import axios from 'axios';

function getStorage() {
  const arrLength = parseInt(localStorage.getItem('arrLength'), 10) || 0;
  const result = [];
  for (let i = 0; i < arrLength; i += 1) {
    const key = `item${i}`;
    const taskId = localStorage.getItem(key);
    if (taskId !== null) {
      result.push(taskId);
    }
  }
  return result;
}

function rmFromStorage(toRemoveId) {
  const arrLength = parseInt(localStorage.getItem('arrLength'), 10) || 0;
  for (let i = 0; i < arrLength; i += 1) {
    const key = `item${i}`;
    const taskId = localStorage.getItem(key);
    if (taskId === toRemoveId) {
      localStorage.removeItem(key);
    }
  }
}
function pushToStorage(value) {
  const arrLength = parseInt(localStorage.getItem('arrLength'), 10) || 0;
  const key = `item${arrLength}`;
  localStorage.setItem(key, value);
  localStorage.setItem('arrLength', JSON.stringify(arrLength + 1));
}

export default {
  name: 'Tasks',
  data() {
    return {
      tasks: [],
      tasksIds: [],
      addTaskIdForm: '',
    };
  },
  created() {
    this.apiUrl = `http://${window.location.hostname}:5000`;
    this.tasksIds = getStorage();
    this.refreshAllTasks();
  },
  methods: {
    submitId() {
      const url = `${this.apiUrl}/checkState`;
      const payload = {
        id: this.addTaskIdForm,
      };
      axios.post(url, payload).then(() => {
        pushToStorage(payload.id);
        this.refreshAllTasks();
      }).catch((error) => {
        this.$notify({
          type: 'error',
          title: 'Connection error with Api server',
          text: error,
        });
      });
    },
    refreshAllTasks() {
      const url = `${this.apiUrl}/checkState`;
      const payload = {
        id: [],
      };
      this.tasksIds.forEach((taskId) => {
        payload.id.push(taskId);
      });
      axios.post(url, payload)
        .then((res) => {
          this.tasks = res.data;
        }).catch((error) => {
          if (error.response.status === 404) {
            this.$notify({
              type: 'error',
              title: 'Task with given ID was not found!',
              text: error,
            });
          } else {
            this.$notify({
              type: 'error',
              title: 'Connection error with api server',
              text: error,
            });
          }
        });
    },
    removeTask(index) {
      rmFromStorage(this.tasksIds[index]);
      this.tasks.splice(index, 1);
      this.tasksIds.splice(index, 1);
    },
    isTaskFailed(index) {
      return this.tasks[index].state !== 'FAILURE';
    },
    isTaskDone(index) {
      return this.tasks[index].state === 'SUCCESS';
    },
    download(index) {
      window.location.href = `${this.apiUrl}/downloadResult/${this.tasks[index].filename}`;
    },
  },
};
</script>
