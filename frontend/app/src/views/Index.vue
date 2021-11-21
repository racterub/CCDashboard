<template>
  <el-container v-if="loggedIn">
    <el-main>
      <el-row :gutter="20">
        <el-col :span="6" :xs="24">
          <el-card class="box-card overview" :class="overviewColor">
            <h5>資產總覽</h5>
            <p>總投資: {{ assetCost.toFixed(3) }} USDT</p>
            <p>總價值: {{ assetValue.toFixed(3) }} USDT</p>
            <p>損益: {{ assetChange.toFixed(3) }} USDT</p>
            <p>損益率: {{ ((assetChange / assetCost) * 100).toFixed(3) }} %</p>
          </el-card>
        </el-col>
        <el-col :span="6" :xs="24">
          <el-card class="box-card">
            <apexchart
              height="200px"
              type="donut"
              :options="pieOptions"
              :series="pieSeries"
            />
          </el-card>
        </el-col>
        <el-col :span="12" :xs="24">
          <el-card class="box-card">
            <apexchart
              type="area"
              height="200px"
              :options="areaOptions"
              :series="areaSeries"
            ></apexchart>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
    <el-footer>
      <el-card class="box-card">
        <el-table
          :data="tableData"
          style="width: 100%"
          height="300px"
          :row-class-name="tableRowClassName"
        >
          <el-table-column prop="coin" label="幣種"> </el-table-column>
          <el-table-column prop="change" sortable label="損益">
          </el-table-column>
          <el-table-column prop="cost" sortable label="成本/顆">
          </el-table-column>
          <el-table-column
            prop="current_price"
            sortable
            label="現價"
          ></el-table-column>
          <el-table-column prop="current_cost" sortable label="當前價值">
          </el-table-column>
          <el-table-column prop="amount" sortable label="持有顆數">
          </el-table-column>
          <el-table-column prop="uamount" sortable label="投資成本">
          </el-table-column>
          <el-table-column fixed="right" label="交易歷史" width="80">
            <template #default="scope">
              <el-button
                size="mini"
                @click="inspectSpots(scope.$index, scope.row)"
                type="primary"
                plain
                >Show</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-footer>
  </el-container>
  <el-container v-else
    ><el-main>
      <div class="title">
        <h1>Welcome to CCDashboard</h1>
        <h1>Please login first.</h1>
      </div>
    </el-main></el-container
  >
</template>
<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      assetValue: 0,
      assetCost: 0,
      assetChange: 0,
      overviewColor: "ov-warning",
      tableData: [],
      pieOptions: {},
      pieSeries: [],
      areaOptions: {
        legend: {
          show: false,
        },
        title: {
          text: "損益走勢",
          align: "center",
          fontFamily: "Avenir, Helvetica, Arial, sans-serif",
        },
        dataLabels: {
          enabled: false,
        },
        chart: {
          height: "200",
          toolbar: {
            tools: {
              download: false,
              selection: true,
              zoom: true,
              zoomin: true,
              zoomout: true,
              pan: false,
              reset: false,
            },
            autoSelected: "zoom",
          },
        },
        stroke: {
          curve: "smooth",
          width: 1.5,
        },
        fill: {
          type: "gradient",
        },
        xaxis: {
          type: "datetime",
          // Ref: https://github.com/apexcharts/apexcharts.js/issues/110
          labels: {
            datetimeUTC: false,
          },
        },
        tooltip: {
          x: {
            format: "yy/MM/dd - HH:mm",
          },
        },
      },
      areaSeries: [
        {
          name: "Profit",
          data: [],
        },
      ],
    };
  },
  computed: {
    ...mapState({
      loggedIn: (state) => state.user.loggedIn,
    }),
  },
  async created() {
    if (this.$store.state.user.loggedIn) {
      const loading = this.$loading({
        lock: true,
        text: "讀取資料中...",
      });
      const summaryResp = await this.$store.dispatch("getSummary");
      const dashboardResp = await this.$store.dispatch("getDashboard");
      if (!summaryResp.status || !dashboardResp.status) {
        loading.close();
        this.$router.push("/login");
      } else {
        let dataLabels = Array.from(summaryResp.data, (elm) => elm.coin);
        let dataValues = Array.from(summaryResp.data, (elm) =>
          parseFloat(elm.current_cost.toFixed(2))
        );
        let areaData = Array.from(dashboardResp.data, (elm) => [
          elm.update_time,
          elm.change,
        ]);
        this.areaSeries[0].data = areaData;
        this.tableData = summaryResp.data;
        this.pieOptions = {
          title: {
            text: "持有資產",
            align: "center",
            fontFamily: "Avenir, Helvetica, Arial, sans-serif",
          },
          labels: dataLabels,
          plotOptions: {
            pie: {
              donut: {
                labels: {
                  show: true,
                  total: {
                    show: true,
                    fontSize: "15px",
                    label: "總計",
                    formatter: function (w) {
                      return w.globals.seriesTotals.reduce((a, b) => {
                        let tmp = 0;
                        tmp = a + b;
                        return parseFloat(tmp.toFixed(2));
                      }, 0);
                    },
                  },
                },
              },
            },
          },
        };
        this.pieSeries = dataValues;
      }
      loading.close();
    }
  },
  watch: {
    tableData(value) {
      this.assetChange = this.SumDataMapReduce(value.map((el) => el.change));
      this.assetCost = this.SumDataMapReduce(value.map((el) => el.uamount));
      this.assetValue = this.SumDataMapReduce(
        value.map((el) => el.current_cost)
      );
      if (this.assetChange < 0) {
        this.overviewColor = "ov-warning";
      } else {
        this.overviewColor = "ov-success";
      }
    },
  },
  methods: {
    tableRowClassName({ row }) {
      if (row.change < 0) {
        return "warning-row";
      } else if (row.change > 0) {
        return "success-row";
      } else {
        return "";
      }
    },
    inspectSpots(idx, row) {
      this.$router.push(`/spots/${row.coin}`);
    },
    SumDataMapReduce(arr) {
      return arr.reduce((a, b) => a + b);
    },
  },
};
</script>
<style lang="scss" scoped>
.title {
  margin-top: 8em;
}
h1 {
  text-align: center;
  font-size: 40px;
}

.overview {
  text-align: center;
}
h5 {
  margin-top: 0.5em;
}

.ov-success {
  background-color: hsla(100, 54%, 49%, 0.3);
  border-color: hsla(100, 54%, 49%, 0.5);
}
.ov-warning {
  background-color: hsla(0, 87%, 69%, 0.3);
  border-color: hsla(0, 87%, 69%, 0.5);
}
</style>
<style lang="scss">
// Ref: https://github.com/ElemeFE/element/issues/11728
// Don't really understand why the Element-Plus dev team didn't implement bg-color in the framework :/
.el-table .warning-row {
  background: hsl(0, 100%, 91%) !important;
}
.el-table .success-row {
  background: hsl(100, 85%, 82%) !important;
}

.el-card {
  min-height: 260px;
}
</style>
