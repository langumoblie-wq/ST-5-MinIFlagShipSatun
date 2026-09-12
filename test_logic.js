const st5Data = [
  { uid: '1', score: 10, timestamp: 1000 },
  { uid: '1', score: 5, timestamp: 3000 },
  { uid: '2', score: 15, timestamp: 1000 },
  { uid: '2', score: 12, timestamp: 4000 }
];

const behaviorData = [
  { targetUid: '1', timestamp: 2000, selections: { desirable: ['good'] } },
  { targetUid: '2', timestamp: 5000, selections: { desirable: ['good'] } }
];

const students = [{ id: '1', name: 'A' }, { id: '2', name: 'B' }];

const comparison = students.map(student => {
    const studentSt5 = st5Data.filter(d => d.uid === student.id).sort((a, b) => a.timestamp - b.timestamp);
    const studentBeh = behaviorData.filter(d => d.targetUid === student.id && d.selections?.desirable?.length > 0).sort((a, b) => a.timestamp - b.timestamp);
    
    if (studentSt5.length >= 2 && studentBeh.length >= 1) {
        const firstInterventionTime = studentBeh[0].timestamp;
        
        // Latest ST5 before or at intervention
        const preTest = [...studentSt5].reverse().find(s => s.timestamp <= firstInterventionTime);
        // First ST5 after intervention
        const postTest = studentSt5.find(s => s.timestamp > firstInterventionTime);
        
        if (preTest && postTest) {
            return {
                student,
                preScore: preTest.score,
                postScore: postTest.score,
                diff: postTest.score - preTest.score,
                interventionTime: firstInterventionTime
            };
        }
    }
    return null;
}).filter(Boolean);

console.log(comparison);
