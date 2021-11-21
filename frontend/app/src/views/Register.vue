<template>
  <el-container>
    <el-main>
      <el-card>
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="帳戶名">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="帳號">
            <el-input v-model="form.username"></el-input>
          </el-form-item>
          <el-form-item label="密碼">
            <el-input v-model="form.password" show-password></el-input>
          </el-form-item>
          <el-form-item label="幣安 API Key">
            <el-input v-model="form.api_key"></el-input>
          </el-form-item>
          <el-form-item label="密碼">
            <el-input v-model="form.api_secret" show-password></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">註冊</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>
<script>
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { ElMessage } from "element-plus";

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
        api_key: "",
        api_secret: "",
        name: "",
      },
    };
  },
  methods: {
    async onSubmit() {
      const loading = this.$loading({
        lock: true,
        text: "註冊中",
      });
      const res = await this.$store.dispatch("sendRegister", {
        name: this.form.name,
        username: this.form.username,
        password: this.form.password,
        api_key: this.form.api_key,
        api_secret: this.form.api_secret,
      });
      loading.close();
      if (res.status) {
        ElMessage.success(res.msg);
        this.$router.push("/");
      } else {
        ElMessage.error(res.msg);
      }
    },
  },
};
</script>
<style lang="scss" scoped></style>
