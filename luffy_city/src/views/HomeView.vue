<template>
  <div class="home">
    <Header></Header>
    <Banner></Banner>
    <el-row>
  <el-col :span="6" v-for="(o, index) in 8" :key="o" class="course_detail">
    <el-card :body-style="{ padding: '0px' }">
      <img src="https://tva1.sinaimg.cn/large/e6c9d24egy1h1g0zd133mj20l20a875i.jpg" class="image">
      <div style="padding: 14px;">
        <span>推荐的课程</span>
        <div class="bottom clearfix">
          <time class="time">价格:999</time>
          <el-button type="text" class="button">查看详情</el-button>
        </div>
      </div>
    </el-card>
  </el-col>
</el-row>
    <img src="https://tva1.sinaimg.cn/large/e6c9d24egy1h1g112oiclj224l0u0jxl.jpg" alt="" height="500px" width="100%">
    <Footer></Footer>
  </div>
</template>

<script>
import Header from '@/components/Header'
import Banner from '@/components/Banner'
import Footer from '@/components/Footer'

export default {
  name: 'HomeView',
  data() {
    return {
      currentDate: new Date()
    }
  },
  components: {
    Header, Banner, Footer
  }
}
</script>

<style scoped>
  .time {
    font-size: 13px;
    color: #999;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }

  .clearfix:after {
      clear: both
  }
  .course_detail{
    padding: 50px;
  }
</style>
