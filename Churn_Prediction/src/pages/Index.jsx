import { ExternalLink, Database, Target, FlaskConical, ChartBar } from "lucide-react";
import SectionCard from "../components/SectionCard.jsx";

const Index = () => {
  return (
    <div className="min-h-screen bg-background relative overflow-hidden ">
      {/* Background gradient orb */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-primary/5 rounded-full blur-3xl animate-glow-pulse pointer-events-none" />
      
      <main className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 py-12 md:py-20">
        {/* Hero Section */}
        <header className="text-center mb-16 animate-fade-in">
          <div className="inline-block px-4 py-1.5 bg-primary/10 border border-primary/20 rounded-full text-primary text-sm font-medium mb-6">
            Machine Learning Research
          </div>
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-bright leading-tight mb-6">
            Customer Churn Prediction<br />
            <span className="text-gradient">Using Machine Learning</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            A Comparative Study on Predicting Customer Behavior with Baseline Classification Models
          </p>
        </header>

        {/* Abstract */}
        <SectionCard title="Abstract" delay={100}>
          <p>
            Customer churn prediction is a critical task for subscription-based businesses, as retaining existing customers is often more cost-effective than acquiring new ones. This study presents a comprehensive machine learning-based framework for predicting customer churn using baseline classification models, benchmarking their performance, and analyzing feature importance. The work focuses on understanding customer behavior patterns that lead to churn and evaluating the effectiveness of various machine learning algorithms.
          </p>
        </SectionCard>

        {/* Objectives */}
        <SectionCard title="Objectives" className="mt-6" delay={200}>
          <ul className="space-y-3">
            {[
              "Analyze customer churn behavior using historical customer data",
              "Build baseline machine learning models for churn prediction",
              "Compare model performance using standard evaluation metrics",
              "Identify and interpret the most influential features contributing to customer churn",
              "Provide insights that can support data-driven retention strategies"
            ].map((objective, index) => (
              <li key={index} className="flex items-start gap-3">
                <Target className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
                <span>{objective}</span>
              </li>
            ))}
          </ul>
        </SectionCard>

        {/* Dataset */}
        <SectionCard title="Dataset" className="mt-6" delay={300}>
          <div className="flex items-start gap-3 mb-4">
            <Database className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
            <p>
              <strong className="text-bright">Telco Customer Churn Dataset</strong> — Contains demographic details, service usage information, contract types, billing methods, and churn labels. Key attributes include tenure, monthly charges, total charges, contract type, payment method, and service subscriptions.
            </p>
          </div>
          <a
            href="https://www.kaggle.com/datasets/blastchar/telco-customer-churn"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary/10 hover:bg-primary/20 border border-primary/30 rounded-lg text-primary font-medium transition-all duration-300 glow-primary hover:scale-[1.02]"
          >
            <ExternalLink className="w-4 h-4" />
            Access Dataset on Kaggle
          </a>
        </SectionCard>

        {/* Methodology */}
        <SectionCard title="Methodology" className="mt-6" delay={400}>
          <div className="space-y-4">
            <div className="flex items-start gap-3">
              <FlaskConical className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
              <p>
                <strong className="text-bright">Data Preprocessing:</strong> Handling missing values, encoding categorical variables, and feature scaling followed by exploratory data analysis.
              </p>
            </div>
            <div className="flex items-start gap-3">
              <ChartBar className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
              <p>
                <strong className="text-bright">Model Training:</strong> Multiple baseline models including Logistic Regression, Decision Trees, Random Forests, and Support Vector Machines evaluated using accuracy, precision, recall, F1-score, and ROC-AUC.
              </p>
            </div>
          </div>
        </SectionCard>

        {/* Expected Results */}
        <SectionCard title="Expected Results & Conclusion" className="mt-6" delay={500}>
          <p className="mb-4">
            Ensemble-based approaches such as Random Forests are anticipated to outperform simpler baseline models. Feature importance analysis is expected to highlight critical factors including <span className="text-primary font-medium">contract type</span>, <span className="text-primary font-medium">customer tenure</span>, <span className="text-primary font-medium">monthly charges</span>, and <span className="text-primary font-medium">payment methods</span>.
          </p>
          <p>
            The proposed framework achieves reliable predictive performance while providing interpretable and actionable insights for customer relationship management and targeted retention strategies.
          </p>
        </SectionCard>

        {/* Footer */}
        <footer className="mt-16 text-center text-muted-foreground text-sm animate-fade-in" style={{ animationDelay: "600ms" }}>
          <div className="w-16 h-px bg-border mx-auto mb-6" />
          <p>Customer Churn Prediction Study • Machine Learning Research Project</p>
        </footer>
      </main>
    </div>
  );
};

export default Index;