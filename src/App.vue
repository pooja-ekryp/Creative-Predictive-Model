<template>
  <div class="section">
    <div class="container">
      <SimpleUpload />
    </div>
  </div>
</template>

<script>
import SimpleUpload from './SimpleUpload.vue';


export default{
  name: "App",
  components: { SimpleUpload }
}
</script>