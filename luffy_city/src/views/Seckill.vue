<template>
  <div>
    <img src="" alt="" height="300px" width="300px">
    <br>
    <el-button type="danger" plain @click.once="handleClick">秒杀</el-button>
  </div>
</template>

<script>
export default {
  name: "Seckill",
  methods: {
    handleClick() {
      this.$axios.get(this.$settings.base_url + 'user/seckill/').then(res => {
        if (res.data.code == 100) {
          let task_id = res.data.id
          this.$message({
            message: res.data.msg,
            type: 'error'
          });
          // 起个定时任务，每隔5s向后端查询一下是否秒杀成功
          let t = setInterval(() => {
            this.$axios.get(this.$settings.base_url + 'user/get_result/?id=' + task_id).then(
                res => {
                  if (res.data.code == 100 || res.data.code == 101) {  //秒杀结束了，要么成功，要么失败了
                    alert(res.data.msg)
                    // 销毁掉定时任务
                    clearInterval(t)
                  } else if (res.data.code == 102) {
                    //什么事都不干
                  }
                }
            )
          }, 5000)
        }
      })
    }
  }
}
</script>

<style scoped>

</style>