<template>
  <div class="course">
    <Header></Header>
      <div>
        <img src="http://test.liuqingzheng.top/1.png" alt="" width="100%">
        <img src="http://test.liuqingzheng.top/2.png" alt="" width="100%">

      </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "@/components/Header"
import Footer from "@/components/Footer"

export default {
  name: "FreeCourse",
  data() {
    return {
      category: 0,
    }
  },
  components: {
    Header,
    Footer,
  }
}
</script>

