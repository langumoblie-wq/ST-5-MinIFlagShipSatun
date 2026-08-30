import re

with open('src/App.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace global edit UI
old_global_target_ui = """                    <div className="flex items-baseline gap-1">
                        {editingTarget?.id === 'all' ? (
                            <input 
                                type="number"
                                autoFocus
                                defaultValue={overviewStats.target}
                                onBlur={(e) => handleSaveTarget('all', e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSaveTarget('all', e.target.value)}
                                className="w-16 bg-white border border-slate-300 rounded px-1 font-bold text-lg outline-none focus:border-emerald-400"
                            />
                        ) : (
                            <>
                                <span className="text-2xl font-black text-slate-800">{overviewStats.target}</span>
                                <span className="text-[10px] font-bold text-slate-500">คน</span>
                                <button onClick={() => setEditingTarget({ id: 'all', value: overviewStats.target })} className="ml-1 text-slate-300 hover:text-slate-500 no-print">
                                    <Pencil size={12} />
                                </button>
                            </>
                        )}
                    </div>"""

new_global_target_ui = """                    <div className="flex items-baseline gap-1">
                        <span className="text-2xl font-black text-slate-800">{overviewStats.target}</span>
                        <span className="text-[10px] font-bold text-slate-500">คน</span>
                    </div>"""
content = content.replace(old_global_target_ui, new_global_target_ui)

# Replace affil edit UI
old_affil_target_ui = """                                        <div className="flex items-center gap-1 justify-end md:justify-center">
                                            {editingTarget?.id === affil ? (
                                                <input 
                                                    type="number"
                                                    autoFocus
                                                    defaultValue={stats.target}
                                                    onBlur={(e) => handleSaveTarget(affil, e.target.value)}
                                                    onKeyDown={(e) => e.key === 'Enter' && handleSaveTarget(affil, e.target.value)}
                                                    className="w-16 bg-white border border-slate-300 rounded px-1 font-bold text-sm text-center outline-none focus:border-indigo-400"
                                                />
                                            ) : (
                                                <>
                                                    <span className="text-lg font-black text-indigo-700">{stats.target}</span>
                                                    <button onClick={() => setEditingTarget({ id: affil, value: stats.target })} className="text-slate-300 hover:text-slate-500 no-print">
                                                        <Pencil size={12} />
                                                    </button>
                                                </>
                                            )}
                                        </div>"""

new_affil_target_ui = """                                        <div className="flex items-center gap-1 justify-end md:justify-center">
                                            <span className="text-lg font-black text-indigo-700">{stats.target}</span>
                                        </div>"""
content = content.replace(old_affil_target_ui, new_affil_target_ui)

with open('src/App.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
