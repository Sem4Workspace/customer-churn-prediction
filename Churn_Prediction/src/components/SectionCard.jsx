const SectionCard = ({ title, children, className = "", delay = 0 }) => {
  return (
    <div 
      className={`bg-card/50 border border-border/50 rounded-lg p-6 md:p-8 card-glow backdrop-blur-sm animate-fade-in ${className}`}
      style={{ animationDelay: `${delay}ms` }}
    >
      <h2 className="text-xl md:text-2xl font-semibold text-primary mb-4">{title}</h2>
      <div className="text-foreground/85 leading-relaxed">{children}</div>
    </div>
  );
};

export default SectionCard;