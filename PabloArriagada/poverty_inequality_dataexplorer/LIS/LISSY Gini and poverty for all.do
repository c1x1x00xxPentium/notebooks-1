program define make_variables
gen miss_comp = 0
quietly replace miss_comp=1 if dhi==. | hifactor==. | hi33==. | hpub_i==. | hpub_u==. | hpub_a==. | hiprivate==. | hxitsc==.
quietly drop if miss_comp==1
sum dhi [w=hwgt], de
gen mi = hifactor + hiprivate + hi33
gen siti = hifactor + hiprivate + hi33 + hpub_i + hpub_u - hxitsc
gen sa = hifactor + hiprivate + hi33 + hpub_a
foreach var in mi siti sa dhi {
	gen e`var'_b = `var'
	replace e`var'_b = 0 if `var'<0
	* Apply top and bottom codes / outlier detection
	gen e`var'_log=log(e`var'_b)
	* keep negatives and 0 in the overall distribution of non-missing dhi
	replace e`var'_log=0 if e`var'_log==. & e`var'_b!=.
	* detect interquartile range
	cap drop iqr
	cap drop upper_bound
	cap drop lower_bound
	qui sum e`var'_log [w=hwgt],de
	gen iqr=r(p75)-r(p25)
	* detect upper bound for extreme values
	gen upper_bound=r(p75) + (iqr * 3)
	gen lower_bound=r(p25) - (iqr * 3)
	* top code income at upper bound for extreme values
	replace e`var'_b=exp(upper_bound) if e`var'_b>exp(upper_bound)
	* bottom code income at lower bound for extreme values
	replace e`var'_b=exp(lower_bound) if e`var'_b<exp(lower_bound)
	replace e`var'_b = (e`var'_b/(nhhmem^0.5))
}
quietly sum edhi_b [w=hwgt*nhhmem], de
global povline = r(p50)*0.5
end

*lissydata, lis from(1980) to(2020)
lissydata, lis from(1980) to(2020) iso2(cl uk)
local countries "${selected}"

foreach ccyy in `countries' {
	quietly use dhi hifactor hi33 hpublic hpub_a hpub_i hpub_u hiprivate hxitsc hwgt nhhmem grossnet using $`ccyy'h, clear
	quietly make_variables
	foreach var in mi siti sa dhi {
		quietly gen byte poor`var'=(e`var'_b<$povline)
		*Calculate and store gini, relative poverty rate
		quietly ineqdec0 e`var'_b [w=hwgt*nhhmem]
		local gini`var' : di %9.3f r(gini)
		quietly sum poor`var' [w=hwgt*nhhmem]
		local povrate`var' : di %9.2f r(mean)*100
	}
/*Output gini and poverty rate measures as comma separated values. If this is the first country being computed, output a line of column headers first. */
if "`ccyy'" == "at87" di "dataset,gini_mi,gini_siti,gini_sa,gini_dhi,povrate_mi,povrate_siti,povrate_sa,povrate_dhi"
di "`ccyy',`ginimi',`ginisiti',`ginisa',`ginidhi',`povratemi',`povratesiti',`povratesa',`povratedhi'"
}
