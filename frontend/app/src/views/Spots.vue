<template>
  <el-container>
    <el-header>
      <el-page-header
        icon="el-icon-arrow-left"
        :content="this.$route.params.coin"
        style="margin-top: 1em"
        @back="goBack"
      ></el-page-header>
    </el-header>
    <el-main>
      <el-row>
        <el-col :span="24">
          <el-card class="box-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>幣種總覽</span>
              </div>
            </template>
            <el-table :data="summaryData" style="width: 100%">
              <el-table-column prop="change" label="損益"> </el-table-column>
              <el-table-column prop="cost" label="成本/顆"> </el-table-column>
              <el-table-column
                prop="current_price"
                label="現價"
              ></el-table-column>
              <el-table-column prop="current_cost" label="當前價值">
              </el-table-column>
              <el-table-column prop="amount" label="持有顆數">
              </el-table-column>
              <el-table-column prop="uamount" label="投資成本">
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
      <el-divider></el-divider>
      <el-row>
        <el-col :span="24">
          <el-card class="box-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>交易歷史紀錄</span>
              </div>
            </template>
            <el-table
              :data="spotsData"
              style="width: 100%"
              max-height="375"
              :row-class-name="tableRowClassName"
            >
              <el-table-column prop="pair" label="交易對"> </el-table-column>
              <el-table-column prop="amount" label="顆數"> </el-table-column>
              <el-table-column prop="uamount" label="總價值"> </el-table-column>
              <el-table-column prop="commission" label="手續費">
              </el-table-column>
              <el-table-column prop="commission_type" label="手續費幣種">
              </el-table-column>
              <el-table-column prop="tx_type" label="交易類別">
              </el-table-column>
              <el-table-column prop="buy_price" label="購買價格">
              </el-table-column>
              <el-table-column
                prop="trade_time"
                label="交易時間"
                min-width="100"
              ></el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>
<script>
export default {
  async created() {
    const loading = this.$loading({
      lock: true,
      text: "讀取資料中...",
    });
    const spotResp = await this.$store.dispatch("getSpots", {
      coin: this.$route.params.coin,
    });
    const summaryResp = await this.$store.dispatch(
      "getSummary",
      this.$route.params.coin
    );
    if (!spotResp.status || !summaryResp.status) {
      loading.close();
      this.$router.push("/login");
    } else {
      this.spotsData = spotResp.data;
      this.summaryData = [summaryResp.data];
    }
    loading.close();
  },
  data() {
    return {
      spotsData: [],
      summaryData: [],
    };
  },
  watch: {
    spotsData(data) {
      data.forEach((row) => {
        if (row.tx_type) {
          row.tx_type = "Buy";
        } else {
          row.tx_type = "Sell";
        }
        row.pair = `${row.coin}/${row.base}`;
      });
    },
  },
  methods: {
    tableRowClassName({ row }) {
      if (row.tx_type === "Sell") {
        return "warning-row";
      } else if (row.tx_type === "Buy") {
        return "success-row";
      } else {
        return "";
      }
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>
<style lang="scss">
// Ref: https://github.com/ElemeFE/element/issues/11728
// Don't really understand why the Element-Plus dev team didn't implement bg-color in the framework :/
.el-table .warning-row {
  background: hsl(0, 90%, 92%) !important;
}
.el-table .success-row {
  background: hsl(99, 54%, 92%) !important;
}
</style>
