enum Flag { hello }


interface CustomConfig {
    flags: [Flag] | [Flag, Flag] | [Flag, Flag, Flag]
    supervisorTargetModifier: number,
    supervisorUpperQuotaModifier: number,
    maxRank: number | null
}

type PartialConfig = Pick<CustomConfig, "flags"> & Partial<Omit<CustomConfig, "flags">>

const customConfigZero: Omit<CustomConfig, "flags"> = {
    supervisorTargetModifier: 0,
    supervisorUpperQuotaModifier: 0,
    maxRank: null
}

function reify(x: PartialConfig): CustomConfig {
    return { ...customConfigZero, ...x }
}


reify({ flags: [Flag.hello] })


const customAlg: SpaAlgorithm<PartialConfig> = (x, data) => {
    const config = reify(x)
    return doTheThing(config, data)
}



//  Algorithm <X, I, O>
//  SpaAlgorithm <X, SpaInput, SpaOutput>

