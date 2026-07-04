<inferred_schema>
type Config struct {
    Env         string `yaml:"env"`
    DatabaseURL string `yaml:"database_url"`
}
</inferred_schema>
<reproduction_steps>
1. Define yaml struct parsing keys.
2. Load env vars via config parser.
</reproduction_steps>