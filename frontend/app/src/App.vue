<template>
  <el-menu :default-active="this.$route.path" router mode="horizontal">
    <el-menu-item
      v-for="(item, i) in navList"
      :key="i"
      :index="item.name"
      :class="item.right ? 'dock-right' : ''"
    >
      {{ item.navItem }}
    </el-menu-item>
  </el-menu>
  <el-container>
    <router-view />
  </el-container>
</template>

<script>
import { mapState } from "vuex";
import { ElMessage } from "element-plus";

export default {
  methods: {
    login: function () {
      this.$router.push("/login");
    },
  },
  computed: {
    ...mapState({
      loggedIn: (state) => state.user.loggedIn,
      popMsg: (state) => state.popMsg,
    }),
    navList() {
      return this.loggedIn
        ? [
            { navItem: "首頁", name: "/", right: false },
            { navItem: "設定", name: "/settings", right: false },
            { navItem: "登出", name: "/logout", right: true },
          ]
        : [
            { navItem: "首頁", name: "/", right: false },
            { navItem: "登入", name: "/login", right: true },
          ];
    },
  },
  updated() {
    if (this.popMsg.msg) {
      ElMessage({
        type: this.popMsg.type,
        message: this.popMsg.msg,
      });
      this.$store.dispatch("clearPopMsg");
    }
  },
};
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  // text-align: center;
  color: #2c3e50;
}
// REF: https://github.com/ElemeFE/element/issues/9798
.el-menu--horizontal > .el-menu-item.dock-right {
  float: right;
}
</style>
