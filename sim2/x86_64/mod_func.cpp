#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _cadecay_destexhe_reg(void);
extern void _HH_traub_reg(void);
extern void _IL_gutnick_reg(void);
extern void _IM_cortex_reg(void);
extern void _IT_huguenard_reg(void);
extern void _izhi2003a_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"mod/cadecay_destexhe.mod\"");
    fprintf(stderr, " \"mod/HH_traub.mod\"");
    fprintf(stderr, " \"mod/IL_gutnick.mod\"");
    fprintf(stderr, " \"mod/IM_cortex.mod\"");
    fprintf(stderr, " \"mod/IT_huguenard.mod\"");
    fprintf(stderr, " \"mod/izhi2003a.mod\"");
    fprintf(stderr, "\n");
  }
  _cadecay_destexhe_reg();
  _HH_traub_reg();
  _IL_gutnick_reg();
  _IM_cortex_reg();
  _IT_huguenard_reg();
  _izhi2003a_reg();
}

#if defined(__cplusplus)
}
#endif
