<template>
  <div class="hello">
    <h1 style="color:red">{{title}}</h1>
    <h2 style="color:grey">最近更新时间 ：{{last_update_time}}</h2>
    <div class='div100'>
    <span class="text100">股票代码 :</span>
    <input class="input100" v-model="stocknumber" type="text" name="fname">
    <span class="text100">价格 :</span>
    <input class="input100" v-model="targetprice" type="text" name="fname">
    <select class="select100" v-model="optionsvalue">
           <option v-for="(item ,index) of listArray" :value=item.val :key=index>{{item.name}}</option>
        </select>
    <button class="btn100" @click="submitclick" >新增</button>
    </div>
    <div class='div100'>
      <span class="text100">删除任务代号 :</span>
      <input class="input100" v-model="delete_number" type="text" name="fname">
      <button class="btn100" @click="deleteclick" >删除</button>
    </div>
    <div class='div100'>
      <span class="text100">目标邮箱 :</span>
      <input class="input100" style="width:400px;" v-model="targetmail" type="text" name="fname">
      <button class="btn100" @click="resetemailclick" >重设</button>
      <button class="btn100" style="color:red" @click="testmailclick" >测试</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      stocknumber:'600567',
      targetprice:'30.00',
      optionsvalue : 0,
      listArray:[
        {name:'超过这个值',val:0},
        {name:'低于这个值',val:1}
      ],
      title: "股票价格监控",
      targetmail: "948566945@qq.com",
      last_update_time: "2020-01-01",
      delete_number: 1,
    }
  },
  mounted () {
    this.axios
    .get('/gettargetmail')
    .then(response => (this.targetmail = response.data));
    this.axios
    .get('/lastupdatetime')
    .then(response => (this.last_update_time = response.data))
  },
  methods:{
    submitclick() {
      this.axios.get('/add',{
        params: {
          stocknumber:this.stocknumber,
          targetprice:this.targetprice,
          optionsvalue:this.optionsvalue
        }
      }).then(() => {location.reload()})
    },
    deleteclick(){
      this.axios.get('/delete',{
        params: {
          taskid:this.delete_number
        }
      }).then(() => {location.reload()})
    },
    resetemailclick() {
      this.axios.get('/settargetmail',{
        params: {
          emailaddr:this.targetmail
        }
      }).then(() => {location.reload()})
    },
    testmailclick() {
      this.axios.get('/testmail').then(() => {location.reload()})
    }
  }
}
</script>

<style scoped>
.input100 {
  width : 200px;
  height : 45px;
  font-size:36px;
  margin-left:20px;
}
.select100 {
  width : 180px;
  height:45px;
  font-size:26px;
  margin-left:20px;
}
.text100 {
  font-size:30px;
  margin-left:10px;
}
.btn100{
  font-size:30px;
  margin-left:20px;
  color:blue;
}
.div100{
  margin-top:20px;
  margin-bottom:20px;
}
</style>
