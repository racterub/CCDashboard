<script>
export default {
  async created() {
    await this.$store.dispatch("sendLogout");
    this.$router.push("/");
  },
};
</script>
