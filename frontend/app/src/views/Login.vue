<template>
  <el-container>
    <el-main>
      <el-card>
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="帳戶名">
            <el-input
              v-model="form.username"
              @keyup.enter="onSubmit"
            ></el-input>
          </el-form-item>
          <el-form-item label="密碼">
            <el-input
              v-model="form.password"
              show-password
              @keyup.enter="onSubmit"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">登入</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>
<script>
import { useRouter } from "vue-router";
import { useStore } from "vuex";

export default {
  setup() {
    let router = useRouter();
    let store = useStore();

    if (store.getters.checkToken) {
      router.push({ name: "首頁" });
    }
  },
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    async onSubmit() {
      const loading = this.$loading({
        lock: true,
        text: "登入中",
      });
      const res = await this.$store.dispatch("sendLogin", {
        username: this.form.username,
        password: this.form.password,
      });
      loading.close();
      if (res) {
        this.$router.push("/");
      }
    },
  },
};
</script>
