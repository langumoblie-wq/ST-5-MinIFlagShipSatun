import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Add renderBehavior function
search_target2 = """  const renderTable = (isPrint = false) => {"""
insertion2 = """  const renderBehavior = (isPrint = false) => (
      <div className="grid lg:grid-cols-2 gap-6 pt-2">
            {/* Radar Chart (Positive Behaviors) */}
            <div className="space-y-4">
              <h3 className="text-base font-bold text-slate-700 flex items-center gap-2">
                <CheckCircle2 size={18} className="text-teal-400"/> Positive Behavior Radar
              </h3>
              <div className="bg-slate-50/50 p-2 rounded-2xl border border-slate-100 flex flex-col items-center">
                <p className="text-[10px] text-slate-400 w-full mb-1 text-center">จุดแข็งและศักยภาพของเป้าหมาย (Protective Factors)</p>
                <div className="w-full h-64">
                  {isPrint ? (
                    <RadarChart cx={150} cy={120} outerRadius={70} width={300} height={250} data={radarData}>
                      <PolarGrid stroke="#e2e8f0" />
                      <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 10, fontWeight: 'bold' }} />
                      <PolarRadiusAxis angle={30} domain={[0, radarDomainMax]} tick={false} axisLine={false}/>
                      <Radar name="ความถี่พฤติกรรมเชิงบวก" dataKey="A" stroke="#14b8a6" fill="#14b8a6" fillOpacity={radarMaxPos === 0 ? 0 : 0.4} strokeOpacity={radarMaxPos === 0 ? 0 : 1} isAnimationActive={false} />
                    </RadarChart>
                  ) : (
                    <ResponsiveContainer width="100%" height="100%">
                      <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                        <PolarGrid stroke="#e2e8f0" />
                        <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 10, fontWeight: 'bold' }} />
                        <PolarRadiusAxis angle={30} domain={[0, radarDomainMax]} tick={false} axisLine={false}/>
                        <Radar name="ความถี่พฤติกรรมเชิงบวก" dataKey="A" stroke="#14b8a6" fill="#14b8a6" fillOpacity={radarMaxPos === 0 ? 0 : 0.4} strokeOpacity={radarMaxPos === 0 ? 0 : 1} />
                        <Tooltip contentStyle={{borderRadius: '12px', border: 'none'}}/>
                      </RadarChart>
                    </ResponsiveContainer>
                  )}
                </div>
              </div>
              <div className={`mt-2 p-4 bg-teal-50/50 rounded-2xl border border-teal-100 ${isPrint ? '!p-2 !mt-1' : ''}`}>
                <p className={`${isPrint ? 'text-xs' : 'text-sm'} font-medium text-teal-800`}>{positiveInterpretation}</p>
              </div>
            </div>

            {/* Negative Behavior */}
            <div className="space-y-4">
               <h3 className="text-base font-bold text-slate-700 flex items-center gap-2">
                 <AlertCircle size={18} className="text-rose-400"/> Negative Behavior Distribution
               </h3>
               <div className="bg-slate-50/50 p-4 rounded-2xl border border-slate-100 flex flex-col justify-center h-[282px]">
                 <p className="text-[10px] text-slate-400 w-full mb-3 text-center">จัดอันดับความถี่ของพฤติกรรมเสี่ยงและปัญหา (Risk Factors)</p>
                 <div className="space-y-3 overflow-y-auto pr-2">
                    {negativeChartData.slice(0, 5).map((item, idx) => {
                      const maxCount = negativeChartData[0]?.count || 1;
                      const pct = (item.count / maxCount) * 100;
                      let barColor = "bg-rose-500";
                      if (idx > 0 && pct < 70) barColor = "bg-orange-400";
                      if (idx > 2 && pct < 40) barColor = "bg-amber-300";
                      if (item.count === 0) barColor = "bg-slate-200";

                      return (
                        <div key={idx} className="relative">
                          <div className="flex justify-between text-[11px] font-bold text-slate-700 mb-1 relative z-10 px-1">
                             <span>{idx + 1}. {item.name}</span>
                             <span>{item.count > 0 ? `${item.count} ครั้ง` : '-'}</span>
                          </div>
                          <div className="w-full bg-slate-100 h-5 rounded-md overflow-hidden relative">
                            <div className={`h-full ${barColor} ${isPrint ? '' : 'transition-all duration-1000'}`} style={{ width: `${item.count === 0 ? 0 : Math.max(pct, 5)}%` }}></div>
                          </div>
                        </div>
                      );
                    })}
                 </div>
               </div>
               <div className={`mt-2 p-4 bg-rose-50/50 rounded-2xl border border-rose-100 ${isPrint ? '!p-2 !mt-1' : ''}`}>
                 <p className={`${isPrint ? 'text-xs' : 'text-sm'} font-medium text-rose-800`}>{negativeInterpretation}</p>
               </div>
            </div>
      </div>
  );

  const renderTable = (isPrint = false) => {"""

if search_target2 in content:
    content = content.replace(search_target2, insertion2)
    print("Added renderBehavior")
else:
    print("Could not find renderTable")

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
