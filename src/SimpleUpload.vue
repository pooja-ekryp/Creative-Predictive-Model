<template>
    <div>
        <div class = "file">
            <form @submit.prevent="onSubmit" enctype="multipart/form-data">
                <div class="fields">
                    <div class="file is-boxed is-primary">
                        <label class="file-label">
                           <input
                            type="file"
                            ref="file"
                            @change="onSelect"
                            class="file-input"
                           /> 
                           <span class="file-cta">
                            <span class="file-icon">
                                <i class="fas fa-upload"></i> 
                            </span>

                            <span class="file-label">
                                Choose a file...
                            </span>
                           </span>
                           
                           <span v-if="file" class="file-name">{{ file.name }}</span>

                        </label>
                    </div>
                </div>
                <div class="fields"><br />
                    <button class="button is-info">Submit</button>
                </div>
                <div class="message">
                    <h5>{{message}}</h5>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
//import axios from 'axios';
export default{
  name: "SimpleUpload",
  data() {
      return {
          file:"",
          message:""
      }
  },
  methods: {
      onSelect(){
          const file = this.$refs.file.files[0];
          this.file = file;
      },
       onSubmit(){
           /*eslint-env node*/
           //console.log('Onsubmit');
          const formData = new FormData();
          formData.append('file',this.file);
          try{
              fetch('http://127.0.0.1:5000/',{method: 'POST',body: formData}).then(response=>{console.log(response)});
              //fetch('http://127.0.0.1:5000/',{method: 'POST',body: formData});
          }
          catch(err){
              //console.log(err);
              //this.message = 'Something went wrong!!'
          }
      }
  },
}
</script>