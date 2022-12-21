<template>
  <div class="banner">
    <el-carousel :interval="5000" arrow="always" height="400px">
      <el-carousel-item v-for="item in bannerList" :key="item.title">
        <div v-if="item.image.indexOf('http')==-1">
          <router-link :to="item.link"><img :src="item.image" alt=""></router-link>
        </div>
        <div v-else>
          <a href=""><img :src="item.image" alt=""></a>
        </div>
      </el-carousel-item>
    </el-carousel>

  </div>

</template>

<script>
export default {
  name: "Banner",
  data() {
    return {
      bannerList: []
    }
  },
  created() {
    this.$axios.get(this.$settings.base_url + 'home/banner/').then(res => {
      this.bannerList = res.data.result
    })
  }
}
</script>

<style scoped>
.el-carousel__item {
  height: 400px;
  min-width: 1200px;
}

.el-carousel__item img {
  height: 400px;
  margin-left: calc(50% - 1920px / 2);
}

.el-carousel__item h3 {
  color: #475669;
  font-size: 18px;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}
</style>