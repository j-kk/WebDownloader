<template>
    <div class="row">
      <div class="container">
        <h1>Create new task</h1>
        <hr><br>
        <div class="card-columns">
          <div class="card">
            <div class="card-header">
              Text task
            </div>
            <div class="card-body">
              <div class="card-title">Download text from site</div>
              <b-form class="card-text">
                <b-form-group label="URL:"
                              label-for="addTextTaskFormTextInput"
                              label-cols-sm="4"
                              label-cols-lg="3">
                  <b-input id="addTextTaskFormTextInput"
                           type="text"
                           v-model="addTextTaskForm.url"
                           class="mb-2 mr-sm-2 mb-sm-0"
                           >Task</b-input>
                </b-form-group>
                  <b-button type="default" @click.prevent="submitTextTask" variant="primary">
                    Submit</b-button>
              </b-form>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              Image task
            </div>
            <div class="card-body">
              <div class="card-title">Download images from site</div>
              <b-form class="card-text">
                <b-form-group label="URL:"
                              label-for="addImageTaskFormTextInput"
                              label-cols-sm="4"
                              label-cols-lg="3">
                  <b-input id="addImageTaskFormTextInput"
                           type="text"
                           v-model="addImageTaskForm.url"
                           class="mb-2 mr-sm-2 mb-sm-0"
                  >Task</b-input>

                </b-form-group>
                <b-button type="default" @click.prevent="submitImageTask" variant="primary">
                  Submit</b-button>
              </b-form>
            </div>
          </div>
          <div class="card">
            <div class="card-header">
              Web crawl task
            </div>
            <div class="card-body">
              <div class="card-title">Create links map</div>
              <b-form id="add" class="card-text">
                <b-form-group label="URL:"
                              label-cols-sm="4"
                              label-cols-lg="3">
                  <b-input type="text"
                           v-model="webCrawlTaskForm.url"
                           class="mb-2 mr-sm-2 mb-sm-0"
                  >Task</b-input>
                </b-form-group>
                <b-button type="default" @click.prevent="submitWebCrawlTask" variant="primary">
                  Submit</b-button>
              </b-form>
            </div>
          </div>
        </div>

      </div>
    </div>
</template>

<script>
/* eslint no-debugger: "warn" */

import axios from 'axios';
import qs from 'qs';

function pushToStorage(value) {
  const arrLength = parseInt(localStorage.getItem('arrLength'), 10) || 0;
  const key = `item${arrLength}`;
  localStorage.setItem(key, value);
  localStorage.setItem('arrLength', JSON.stringify(arrLength + 1));
}

export default {
  name: 'Main',
  title: 'Nowe zadanie',
  components: {
  },
  data() {
    return {
      addTextTaskForm: {
        url: '',
      },
      addImageTaskForm: {
        url: '',
      },
      webCrawlTaskForm: {
        url: '',
      },
      apiUrl: '',
    };
  },
  created() {
    if (process.env.NODE_ENV === 'development') {
      this.apiUrl = `http://${window.location.hostname}:5000`;
    } else {
      this.apiUrl = `http://${window.location.hostname}/api`;
    }
  },
  methods: {
    showID(task, type) {
      pushToStorage(task.task_id);
      this.$notify({
        title: `New ${type} task added`,
        text: `ID: ${task.task_id}\nURL: ${task.url}`,
        icon: 'info_outline',
      });
    },
    submitTask(value, urlSuffix, taskName) {
      const path = `${this.apiUrl}/${urlSuffix}`;
      if (value.url.length > 0) {
        const payload = {
          url: [value.url],
        };
        const options = {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          data: payload,
          url: path,
        };
        axios(options).then((result) => {
          result.data.forEach((task) => {
            this.showID(task, 'text');
          });
        }).catch((error) => {
          this.$notify({
            type: 'error',
            title: 'Connection error with Api server',
            text: error,
          });
        });
      } else {
        this.$notify({
          type: 'error',
          title: `Download ${taskName} task`,
          text: 'URL field is empty',
        });
      }
    },
    submitTextTask() {
      this.submitTask(this.addTextTaskForm, 'getText', 'text');
    },
    submitImageTask() {
      this.submitTask(this.addImageTaskForm, 'getImages', 'images');
    },
    submitWebCrawlTask() {
      this.submitTask(this.webCrawlTaskForm, 'crawlWebsite', 'crawl website');
    },
  },
};
</script>

<style scoped>

</style>
