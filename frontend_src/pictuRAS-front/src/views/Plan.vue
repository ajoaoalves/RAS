<template>
    <div class="plans-view">
      <h1>Escolha o seu Plano de Subscrição</h1>
      <div class="plans-container">
        <PlanCard
          v-for="plan in plans"
          :key="plan.id"
          :name="plan.name"
          :description="plan.description"
          :price="plan.price"
          :buttonText="plan.buttonText"
          :onClick="() => selectPlan(plan.id)"
        />
      </div>
    </div>
</template>

<script>
import PlanCard from '../components/PlanCard.vue';

export default {
  name: "PlansView",
  components: {
    PlanCard,
  },
  data() {
    return {
      plans: [
        {
          id: 1,
          name: "Plano Gratuito",
          description: [
            "Basic features with limited storage and tools.",
            "Ideal for individuals starting out."
          ],
          price: "Free",
          buttonText: "Select Free Plan",
        },
        {
          id: 2,
          name: "Premium Plan",
          description: [
            "Unlock all tools and get unlimited storage.",
            "Perfect for professionals who need advanced features."
          ],
          price: "$9.99/month",
          buttonText: "Upgrade to Premium",
        },
        {
          id: 3,
          name: "Annual Plan",
          description: [
            "Save more with a yearly subscription.",
            "Get the best value for long-term commitment."
          ],
          price: "$99.99/year",
          buttonText: "Choose Annual Plan",
        },
      ],
    };
  },
  methods: {
    selectPlan(planId) {
      console.log(`Selected Plan ID: ${planId}`);
      // Extend this method for API calls or routing
    },
  },
};
</script>

<style scoped>
.plans-view {
  text-align: center;
  padding: 20px;
}

.plans-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}
</style>
