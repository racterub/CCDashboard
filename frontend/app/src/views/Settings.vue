<template>
  <el-container>
    <el-main>
      <el-tabs type="border-card">
        <el-tab-pane label="帳戶設定"
          ><el-form ref="form" :model="userForm" label-width="80px">
            <el-form-item>
              <div>
                <p>Logged in as {{ name }}</p>
              </div>
            </el-form-item>
            <el-form-item label="舊密碼">
              <el-input v-model="userForm.oldPassword" show-password></el-input>
            </el-form-item>
            <el-form-item label="新密碼">
              <el-input v-model="userForm.newPassword" show-password></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="updatePassword">更新</el-button>
            </el-form-item>
          </el-form></el-tab-pane
        >
        <el-tab-pane label="Binance 設定" disabled>
          <el-form ref="form" :model="binanceForm" label-width="80px">
            <el-form-item label="Key">
              <el-input v-model="binanceForm.apiKey"></el-input>
            </el-form-item>
            <el-form-item label="Secret">
              <el-input
                v-model="binanceForm.apiSecret"
                show-password
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="updateBinance">更新</el-button>
            </el-form-item>

            <el-form-item>
              <div>
                <p 帳戶 class="green-dot">帳戶 API 狀態</p>
                <el-button size="mini" type="primary" @click="updateBinance"
                  >檢查</el-button
                >
              </div>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="FTX 設定" disabled></el-tab-pane>
      </el-tabs>
    </el-main>
  </el-container>
</template>
<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      APIStatus: "red-dot",
      userForm: {
        oldPassword: "",
        newPassword: "",
      },
      binanceForm: {
        apiKey: "",
        apiSecret: "",
      },
    };
  },
  computed: {
    ...mapState({
      name: (state) => state.user.name,
    }),
  },
  async created() {
    const resp = await this.$store.dispatch("checkAccount");
    if (resp) {
      this.APIStatus = "green-dot";
    } else {
      this.APIStatus = "red-dot";
    }
  },
  methods: {
    async updatePassword() {
      const resp = await this.$store.dispatch("updatePassword", {
        newPassword: this.userForm.newPassword,
        oldPassword: this.userForm.oldPassword,
      });
      if (resp.status) {
        this.userForm.newPassword = "";
        this.userForm.oldPassword = "";
      } else {
        if (resp.auth) {
          this.$router.push("/");
        }
      }
    },
    // async updateBinance() {
    //   const resp = await this.$store.dispatch("updateBinance", {
    //     newAPIKey: this.binanceForm.apiKey,
    //     newAPISecret: this.binanceForm.apiSecret,
    //   });
    //   if (resp.status) {
    //     ElMessage.success(resp.msg);
    //     this.binanceForm.apiKey = "";
    //     this.binanceForm.apiSecret = "";
    //   } else {
    //     if (resp.auth) {
    //       ElMessage.error(resp.msg);
    //       this.$store.dispatch("userLogout");
    //       this.$router.push("/login");
    //     } else {
    //       ElMessage.error(resp.msg);
    //     }
    //   }
    // },
  },
};
</script>
<style lang="scss" scoped>
.red-dot::after {
  content: "";
  margin-left: 0.5em;
  height: 10px;
  width: 10px;
  border-radius: 50%;
  display: inline-block;
  border: 1px solid rgb(214, 97, 107);
  background-color: rgba(214, 97, 107, 0.5);
  animation: pulsate 2s ease-out;
  animation-iteration-count: infinite;
  opacity: 0.5;
}

.green-dot::after {
  content: "";
  margin-left: 0.5em;
  margin-top: 0.5em;
  height: 10px;
  width: 10px;
  border-radius: 50%;
  display: inline-block;
  border: 1px solid rgb(108, 204, 60);
  background-color: rgba(45, 199, 45, 0.5);
  animation: pulsate 2s ease-out;
  animation-iteration-count: infinite;
  opacity: 0.5;
}

@keyframes pulsate {
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.5;
  }
}
</style>
