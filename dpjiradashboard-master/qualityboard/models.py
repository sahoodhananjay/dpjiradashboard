from django.db import models

month_options = (
                ('January','January'),
                ('February','February'),
                ('March','March'),
                ('April','April'),
                ('May','May'),
                ('June','June'),
                ('July','July'),
                ('August','August'),
                ('September','September'),
                ('October','October'),
                ('November','November'),
                ('December','December'),
                )


class DP(models.Model):

    One = models.CharField(max_length=5, blank=True)
    Two = models.CharField(max_length=5, blank=True)
    Three = models.CharField(max_length=5, blank=True)
    Four = models.CharField(max_length=5, blank=True)
    Five = models.CharField(max_length=5, blank=True)
    Six = models.CharField(max_length=5, blank=True)
    Seven = models.CharField(max_length=5, blank=True)
    Eight = models.CharField(max_length=5, blank=True)
    Nine = models.CharField(max_length=5, blank=True)
    Ten = models.CharField(max_length=5, blank=True)
    Eleven = models.CharField(max_length=5, blank=True)
    Twelve = models.CharField(max_length=5, blank=True)
    Thirteen = models.CharField(max_length=5, blank=True)
    Fourteen = models.CharField(max_length=5, blank=True)
    Fifteen = models.CharField(max_length=5, blank=True)
    Sixteen = models.CharField(max_length=5, blank=True)
    Seventeen = models.CharField(max_length=5, blank=True)
    Eighteen = models.CharField(max_length=5, blank=True)
    Nineteen = models.CharField(max_length=5, blank=True)
    Twenty = models.CharField(max_length=5, blank=True)
    Twentyone = models.CharField(max_length=5, blank=True)
    Twentytwo = models.CharField(max_length=5, blank=True)
    Twentythree = models.CharField(max_length=5, blank=True)
    Twentyfour = models.CharField(max_length=5, blank=True)
    Twentyfive = models.CharField(max_length=5, blank=True)
    Twentysix = models.CharField(max_length=5, blank=True)
    Twentyseven = models.CharField(max_length=5, blank=True)
    Twentyeight = models.CharField(max_length=5, blank=True)
    Twentynine = models.CharField(max_length=5, blank=True)
    Thirty = models.CharField(max_length=5, blank=True)
    Thirtyone = models.CharField(max_length=5, blank=True)
    AccountBilling = models.CharField(max_length=5, blank=True)
    Analytics = models.CharField(max_length=5, blank=True)
    BackendInfrastructure = models.CharField(max_length=5, blank=True)
    CallExperience = models.CharField(max_length=5, blank=True)
    CallingFeatures = models.CharField(max_length=5, blank=True)
    ContactCenter = models.CharField(max_length=5, blank=True)
    CustomerAgentAssist = models.CharField(max_length=5, blank=True)
    DataInsights = models.CharField(max_length=5, blank=True)
    DeveloperPlatform = models.CharField(max_length=5, blank=True)
    Devices = models.CharField(max_length=5, blank=True)
    DialpadTalk = models.CharField(max_length=5, blank=True)
    DigitalExperience = models.CharField(max_length=5, blank=True)
    EngineeringProductivity = models.CharField(max_length=5, blank=True)
    FrontendInfrastructure = models.CharField(max_length=5, blank=True)
    Growth = models.CharField(max_length=5, blank=True)
    Integrations = models.CharField(max_length=5, blank=True)
    Messaging = models.CharField(max_length=5, blank=True)
    Mobile = models.CharField(max_length=5, blank=True)
    ProductionSupport = models.CharField(max_length=5, blank=True)
    UberConference = models.CharField(max_length=5, blank=True)
    VoiceIntelligence = models.CharField(max_length=5, blank=True)
    Website = models.CharField(max_length=5, blank=True)
    Backlog = models.CharField(max_length=20, blank=True)
    Blocked = models.CharField(max_length=20, blank=True)
    CodeReview = models.CharField(max_length=20, blank=True)
    Closed = models.CharField(max_length=20, blank=True)
    InProgress = models.CharField(max_length=20, blank=True)
    NeedsTriage = models.CharField(max_length=20, blank=True)
    Open = models.CharField(max_length=20, blank=True)
    ReadyforTesting = models.CharField(max_length=20, blank=True)
    ReadyforProduction = models.CharField(max_length=20, blank=True)
    ToDo = models.CharField(max_length=20, blank=True)
    LastUpdate = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f" {self.id}: {self.One} {self.Two} {self.Three} {self.Four} {self.Five} {self.Six} \
                  {self.Seven}: {self.Eight} {self.Nine} {self.Ten} {self.Eleven} {self.Twelve} {self.Thirteen} \
                  {self.Fourteen}: {self.Fifteen} {self.Sixteen} {self.Seventeen} {self.Eighteen} {self.Nineteen} {self.Twenty} \
                  {self.Twentyone}: {self.Twentytwo} {self.Twentythree} {self.Twentyfour} {self.Twentyfive} {self.Twentysix} {self.Twentyseven} \
                  {self.Twentyeight}: {self.Twentynine} {self.Thirty} {self.Thirtyone} {self.AccountBilling} {self.Analytics} {self.BackendInfrastructure} \
                  {self.CallExperience}: {self.CallingFeatures} {self.ContactCenter} {self.CustomerAgentAssist} {self.DataInsights} {self.DeveloperPlatform} {self.Devices} \
                  {self.DialpadTalk}: {self.DigitalExperience} {self.EngineeringProductivity} {self.FrontendInfrastructure} {self.Growth} {self.Integrations} {self.Messaging} {self.Mobile} \
                  {self.ProductionSupport} {self.UberConference} {self.VoiceIntelligence} {self.Website} {self.Backlog} {self.Blocked} {self.CodeReview} {self.Closed} \
                  {self.InProgress} {self.NeedsTriage} {self.Open} {self.ReadyforTesting} {self.ReadyforProduction} {self.ToDo} {self.LastUpdate}"



class DPExternal(models.Model):

    One = models.CharField(max_length=5, blank=True)
    Two = models.CharField(max_length=5, blank=True)
    Three = models.CharField(max_length=5, blank=True)
    Four = models.CharField(max_length=5, blank=True)
    Five = models.CharField(max_length=5, blank=True)
    Six = models.CharField(max_length=5, blank=True)
    Seven = models.CharField(max_length=5, blank=True)
    Eight = models.CharField(max_length=5, blank=True)
    Nine = models.CharField(max_length=5, blank=True)
    Ten = models.CharField(max_length=5, blank=True)
    Eleven = models.CharField(max_length=5, blank=True)
    Twelve = models.CharField(max_length=5, blank=True)
    Thirteen = models.CharField(max_length=5, blank=True)
    Fourteen = models.CharField(max_length=5, blank=True)
    Fifteen = models.CharField(max_length=5, blank=True)
    Sixteen = models.CharField(max_length=5, blank=True)
    Seventeen = models.CharField(max_length=5, blank=True)
    Eighteen = models.CharField(max_length=5, blank=True)
    Nineteen = models.CharField(max_length=5, blank=True)
    Twenty = models.CharField(max_length=5, blank=True)
    Twentyone = models.CharField(max_length=5, blank=True)
    Twentytwo = models.CharField(max_length=5, blank=True)
    Twentythree = models.CharField(max_length=5, blank=True)
    Twentyfour = models.CharField(max_length=5, blank=True)
    Twentyfive = models.CharField(max_length=5, blank=True)
    Twentysix = models.CharField(max_length=5, blank=True)
    Twentyseven = models.CharField(max_length=5, blank=True)
    Twentyeight = models.CharField(max_length=5, blank=True)
    Twentynine = models.CharField(max_length=5, blank=True)
    Thirty = models.CharField(max_length=5, blank=True)
    Thirtyone = models.CharField(max_length=5, blank=True)
    AccountBilling = models.CharField(max_length=5, blank=True)
    Analytics = models.CharField(max_length=5, blank=True)
    BackendInfrastructure = models.CharField(max_length=5, blank=True)
    CallExperience = models.CharField(max_length=5, blank=True)
    CallingFeatures = models.CharField(max_length=5, blank=True)
    ContactCenter = models.CharField(max_length=5, blank=True)
    CustomerAgentAssist = models.CharField(max_length=5, blank=True)
    DataInsights = models.CharField(max_length=5, blank=True)
    DeveloperPlatform = models.CharField(max_length=5, blank=True)
    Devices = models.CharField(max_length=5, blank=True)
    DialpadTalk = models.CharField(max_length=5, blank=True)
    DigitalExperience = models.CharField(max_length=5, blank=True)
    EngineeringProductivity = models.CharField(max_length=5, blank=True)
    FrontendInfrastructure = models.CharField(max_length=5, blank=True)
    Growth = models.CharField(max_length=5, blank=True)
    Integrations = models.CharField(max_length=5, blank=True)
    Messaging = models.CharField(max_length=5, blank=True)
    Mobile = models.CharField(max_length=5, blank=True)
    ProductionSupport = models.CharField(max_length=5, blank=True)
    UberConference = models.CharField(max_length=5, blank=True)
    VoiceIntelligence = models.CharField(max_length=5, blank=True)
    Website = models.CharField(max_length=5, blank=True)
    Backlog = models.CharField(max_length=20, blank=True)
    Blocked = models.CharField(max_length=20, blank=True)
    CodeReview = models.CharField(max_length=20, blank=True)
    Closed = models.CharField(max_length=20, blank=True)
    InProgress = models.CharField(max_length=20, blank=True)
    NeedsTriage = models.CharField(max_length=20, blank=True)
    Open = models.CharField(max_length=20, blank=True)
    ReadyforTesting = models.CharField(max_length=20, blank=True)
    ReadyforProduction = models.CharField(max_length=20, blank=True)
    ToDo = models.CharField(max_length=20, blank=True)
    LastUpdate = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f" {self.id}: {self.One} {self.Two} {self.Three} {self.Four} {self.Five} {self.Six} \
                  {self.Seven}: {self.Eight} {self.Nine} {self.Ten} {self.Eleven} {self.Twelve} {self.Thirteen} \
                  {self.Fourteen}: {self.Fifteen} {self.Sixteen} {self.Seventeen} {self.Eighteen} {self.Nineteen} {self.Twenty} \
                  {self.Twentyone}: {self.Twentytwo} {self.Twentythree} {self.Twentyfour} {self.Twentyfive} {self.Twentysix} {self.Twentyseven} \
                  {self.Twentyeight}: {self.Twentynine} {self.Thirty} {self.Thirtyone} {self.AccountBilling} {self.Analytics} {self.BackendInfrastructure} \
                  {self.CallExperience}: {self.CallingFeatures} {self.ContactCenter} {self.CustomerAgentAssist} {self.DataInsights} {self.DeveloperPlatform} {self.Devices} \
                  {self.DialpadTalk}: {self.DigitalExperience} {self.EngineeringProductivity} {self.FrontendInfrastructure} {self.Growth} {self.Integrations} {self.Messaging} {self.Mobile} \
                  {self.ProductionSupport} {self.UberConference} {self.VoiceIntelligence} {self.Website} {self.Backlog} {self.Blocked} {self.CodeReview} {self.Closed} \
                  {self.InProgress} {self.NeedsTriage} {self.Open} {self.ReadyforTesting} {self.ReadyforProduction} {self.ToDo} {self.LastUpdate}"



class DPM(models.Model):

    One = models.CharField(max_length=5, blank=True)
    Two = models.CharField(max_length=5, blank=True)
    Three = models.CharField(max_length=5, blank=True)
    Four = models.CharField(max_length=5, blank=True)
    Five = models.CharField(max_length=5, blank=True)
    Six = models.CharField(max_length=5, blank=True)
    Seven = models.CharField(max_length=5, blank=True)
    Eight = models.CharField(max_length=5, blank=True)
    Nine = models.CharField(max_length=5, blank=True)
    Ten = models.CharField(max_length=5, blank=True)
    Eleven = models.CharField(max_length=5, blank=True)
    Twelve = models.CharField(max_length=5, blank=True)
    Thirteen = models.CharField(max_length=5, blank=True)
    Fourteen = models.CharField(max_length=5, blank=True)
    Fifteen = models.CharField(max_length=5, blank=True)
    Sixteen = models.CharField(max_length=5, blank=True)
    Seventeen = models.CharField(max_length=5, blank=True)
    Eighteen = models.CharField(max_length=5, blank=True)
    Nineteen = models.CharField(max_length=5, blank=True)
    Twenty = models.CharField(max_length=5, blank=True)
    Twentyone = models.CharField(max_length=5, blank=True)
    Twentytwo = models.CharField(max_length=5, blank=True)
    Twentythree = models.CharField(max_length=5, blank=True)
    Twentyfour = models.CharField(max_length=5, blank=True)
    Twentyfive = models.CharField(max_length=5, blank=True)
    Twentysix = models.CharField(max_length=5, blank=True)
    Twentyseven = models.CharField(max_length=5, blank=True)
    Twentyeight = models.CharField(max_length=5, blank=True)
    Twentynine = models.CharField(max_length=5, blank=True)
    Thirty = models.CharField(max_length=5, blank=True)
    Thirtyone = models.CharField(max_length=5, blank=True)
    AccountBilling = models.CharField(max_length=5, blank=True)
    Analytics = models.CharField(max_length=5, blank=True)
    BackendInfrastructure = models.CharField(max_length=5, blank=True)
    CallExperience = models.CharField(max_length=5, blank=True)
    CallingFeatures = models.CharField(max_length=5, blank=True)
    ContactCenter = models.CharField(max_length=5, blank=True)
    CustomerAgentAssist = models.CharField(max_length=5, blank=True)
    DataInsights = models.CharField(max_length=5, blank=True)
    DeveloperPlatform = models.CharField(max_length=5, blank=True)
    Devices = models.CharField(max_length=5, blank=True)
    DialpadTalk = models.CharField(max_length=5, blank=True)
    DigitalExperience = models.CharField(max_length=5, blank=True)
    EngineeringProductivity = models.CharField(max_length=5, blank=True)
    FrontendInfrastructure = models.CharField(max_length=5, blank=True)
    Growth = models.CharField(max_length=5, blank=True)
    Integrations = models.CharField(max_length=5, blank=True)
    Messaging = models.CharField(max_length=5, blank=True)
    Mobile = models.CharField(max_length=5, blank=True)
    ProductionSupport = models.CharField(max_length=5, blank=True)
    UberConference = models.CharField(max_length=5, blank=True)
    VoiceIntelligence = models.CharField(max_length=5, blank=True)
    Website = models.CharField(max_length=5, blank=True)
    Backlog = models.CharField(max_length=20, blank=True)
    Blocked = models.CharField(max_length=20, blank=True)
    CodeReview = models.CharField(max_length=20, blank=True)
    Closed = models.CharField(max_length=20, blank=True)
    InProgress = models.CharField(max_length=20, blank=True)
    NeedsTriage = models.CharField(max_length=20, blank=True)
    Open = models.CharField(max_length=20, blank=True)
    ReadyforTesting = models.CharField(max_length=20, blank=True)
    ReadyforProduction = models.CharField(max_length=20, blank=True)
    ToDo = models.CharField(max_length=20, blank=True)
    LastUpdate = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f" {self.id}: {self.One} {self.Two} {self.Three} {self.Four} {self.Five} {self.Six} \
                  {self.Seven}: {self.Eight} {self.Nine} {self.Ten} {self.Eleven} {self.Twelve} {self.Thirteen} \
                  {self.Fourteen}: {self.Fifteen} {self.Sixteen} {self.Seventeen} {self.Eighteen} {self.Nineteen} {self.Twenty} \
                  {self.Twentyone}: {self.Twentytwo} {self.Twentythree} {self.Twentyfour} {self.Twentyfive} {self.Twentysix} {self.Twentyseven} \
                  {self.Twentyeight}: {self.Twentynine} {self.Thirty} {self.Thirtyone} {self.AccountBilling} {self.Analytics} {self.BackendInfrastructure} \
                  {self.CallExperience}: {self.CallingFeatures} {self.ContactCenter} {self.CustomerAgentAssist} {self.DataInsights} {self.DeveloperPlatform} {self.Devices} \
                  {self.DialpadTalk}: {self.DigitalExperience} {self.EngineeringProductivity} {self.FrontendInfrastructure} {self.Growth} {self.Integrations} {self.Messaging} {self.Mobile} \
                  {self.ProductionSupport} {self.UberConference} {self.VoiceIntelligence} {self.Website} {self.Backlog} {self.Blocked} {self.CodeReview} {self.Closed} \
                  {self.InProgress} {self.NeedsTriage} {self.Open} {self.ReadyforTesting} {self.ReadyforProduction} {self.ToDo} {self.LastUpdate}"



class DPMExternal(models.Model):

    One = models.CharField(max_length=5, blank=True)
    Two = models.CharField(max_length=5, blank=True)
    Three = models.CharField(max_length=5, blank=True)
    Four = models.CharField(max_length=5, blank=True)
    Five = models.CharField(max_length=5, blank=True)
    Six = models.CharField(max_length=5, blank=True)
    Seven = models.CharField(max_length=5, blank=True)
    Eight = models.CharField(max_length=5, blank=True)
    Nine = models.CharField(max_length=5, blank=True)
    Ten = models.CharField(max_length=5, blank=True)
    Eleven = models.CharField(max_length=5, blank=True)
    Twelve = models.CharField(max_length=5, blank=True)
    Thirteen = models.CharField(max_length=5, blank=True)
    Fourteen = models.CharField(max_length=5, blank=True)
    Fifteen = models.CharField(max_length=5, blank=True)
    Sixteen = models.CharField(max_length=5, blank=True)
    Seventeen = models.CharField(max_length=5, blank=True)
    Eighteen = models.CharField(max_length=5, blank=True)
    Nineteen = models.CharField(max_length=5, blank=True)
    Twenty = models.CharField(max_length=5, blank=True)
    Twentyone = models.CharField(max_length=5, blank=True)
    Twentytwo = models.CharField(max_length=5, blank=True)
    Twentythree = models.CharField(max_length=5, blank=True)
    Twentyfour = models.CharField(max_length=5, blank=True)
    Twentyfive = models.CharField(max_length=5, blank=True)
    Twentysix = models.CharField(max_length=5, blank=True)
    Twentyseven = models.CharField(max_length=5, blank=True)
    Twentyeight = models.CharField(max_length=5, blank=True)
    Twentynine = models.CharField(max_length=5, blank=True)
    Thirty = models.CharField(max_length=5, blank=True)
    Thirtyone = models.CharField(max_length=5, blank=True)
    AccountBilling = models.CharField(max_length=5, blank=True)
    Analytics = models.CharField(max_length=5, blank=True)
    BackendInfrastructure = models.CharField(max_length=5, blank=True)
    CallExperience = models.CharField(max_length=5, blank=True)
    CallingFeatures = models.CharField(max_length=5, blank=True)
    ContactCenter = models.CharField(max_length=5, blank=True)
    CustomerAgentAssist = models.CharField(max_length=5, blank=True)
    DataInsights = models.CharField(max_length=5, blank=True)
    DeveloperPlatform = models.CharField(max_length=5, blank=True)
    Devices = models.CharField(max_length=5, blank=True)
    DialpadTalk = models.CharField(max_length=5, blank=True)
    DigitalExperience = models.CharField(max_length=5, blank=True)
    EngineeringProductivity = models.CharField(max_length=5, blank=True)
    FrontendInfrastructure = models.CharField(max_length=5, blank=True)
    Growth = models.CharField(max_length=5, blank=True)
    Integrations = models.CharField(max_length=5, blank=True)
    Messaging = models.CharField(max_length=5, blank=True)
    Mobile = models.CharField(max_length=5, blank=True)
    ProductionSupport = models.CharField(max_length=5, blank=True)
    UberConference = models.CharField(max_length=5, blank=True)
    VoiceIntelligence = models.CharField(max_length=5, blank=True)
    Website = models.CharField(max_length=5, blank=True)
    Backlog = models.CharField(max_length=20, blank=True)
    Blocked = models.CharField(max_length=20, blank=True)
    CodeReview = models.CharField(max_length=20, blank=True)
    Closed = models.CharField(max_length=20, blank=True)
    InProgress = models.CharField(max_length=20, blank=True)
    NeedsTriage = models.CharField(max_length=20, blank=True)
    Open = models.CharField(max_length=20, blank=True)
    ReadyforTesting = models.CharField(max_length=20, blank=True)
    ReadyforProduction = models.CharField(max_length=20, blank=True)
    ToDo = models.CharField(max_length=20, blank=True)
    LastUpdate = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f" {self.id}: {self.One} {self.Two} {self.Three} {self.Four} {self.Five} {self.Six} \
                  {self.Seven}: {self.Eight} {self.Nine} {self.Ten} {self.Eleven} {self.Twelve} {self.Thirteen} \
                  {self.Fourteen}: {self.Fifteen} {self.Sixteen} {self.Seventeen} {self.Eighteen} {self.Nineteen} {self.Twenty} \
                  {self.Twentyone}: {self.Twentytwo} {self.Twentythree} {self.Twentyfour} {self.Twentyfive} {self.Twentysix} {self.Twentyseven} \
                  {self.Twentyeight}: {self.Twentynine} {self.Thirty} {self.Thirtyone} {self.AccountBilling} {self.Analytics} {self.BackendInfrastructure} \
                  {self.CallExperience}: {self.CallingFeatures} {self.ContactCenter} {self.CustomerAgentAssist} {self.DataInsights} {self.DeveloperPlatform} {self.Devices} \
                  {self.DialpadTalk}: {self.DigitalExperience} {self.EngineeringProductivity} {self.FrontendInfrastructure} {self.Growth} {self.Integrations} {self.Messaging} {self.Mobile} \
                  {self.ProductionSupport} {self.UberConference} {self.VoiceIntelligence} {self.Website} {self.Backlog} {self.Blocked} {self.CodeReview} {self.Closed} \
                  {self.InProgress} {self.NeedsTriage} {self.Open} {self.ReadyforTesting} {self.ReadyforProduction} {self.ToDo} {self.LastUpdate}"



class MOB(models.Model):

    One = models.CharField(max_length=5, blank=True)
    Two = models.CharField(max_length=5, blank=True)
    Three = models.CharField(max_length=5, blank=True)
    Four = models.CharField(max_length=5, blank=True)
    Five = models.CharField(max_length=5, blank=True)
    Six = models.CharField(max_length=5, blank=True)
    Seven = models.CharField(max_length=5, blank=True)
    Eight = models.CharField(max_length=5, blank=True)
    Nine = models.CharField(max_length=5, blank=True)
    Ten = models.CharField(max_length=5, blank=True)
    Eleven = models.CharField(max_length=5, blank=True)
    Twelve = models.CharField(max_length=5, blank=True)
    Thirteen = models.CharField(max_length=5, blank=True)
    Fourteen = models.CharField(max_length=5, blank=True)
    Fifteen = models.CharField(max_length=5, blank=True)
    Sixteen = models.CharField(max_length=5, blank=True)
    Seventeen = models.CharField(max_length=5, blank=True)
    Eighteen = models.CharField(max_length=5, blank=True)
    Nineteen = models.CharField(max_length=5, blank=True)
    Twenty = models.CharField(max_length=5, blank=True)
    Twentyone = models.CharField(max_length=5, blank=True)
    Twentytwo = models.CharField(max_length=5, blank=True)
    Twentythree = models.CharField(max_length=5, blank=True)
    Twentyfour = models.CharField(max_length=5, blank=True)
    Twentyfive = models.CharField(max_length=5, blank=True)
    Twentysix = models.CharField(max_length=5, blank=True)
    Twentyseven = models.CharField(max_length=5, blank=True)
    Twentyeight = models.CharField(max_length=5, blank=True)
    Twentynine = models.CharField(max_length=5, blank=True)
    Thirty = models.CharField(max_length=5, blank=True)
    Thirtyone = models.CharField(max_length=5, blank=True)
    AccountBilling = models.CharField(max_length=5, blank=True)
    Analytics = models.CharField(max_length=5, blank=True)
    BackendInfrastructure = models.CharField(max_length=5, blank=True)
    CallExperience = models.CharField(max_length=5, blank=True)
    CallingFeatures = models.CharField(max_length=5, blank=True)
    ContactCenter = models.CharField(max_length=5, blank=True)
    CustomerAgentAssist = models.CharField(max_length=5, blank=True)
    DataInsights = models.CharField(max_length=5, blank=True)
    DeveloperPlatform = models.CharField(max_length=5, blank=True)
    Devices = models.CharField(max_length=5, blank=True)
    DialpadTalk = models.CharField(max_length=5, blank=True)
    DigitalExperience = models.CharField(max_length=5, blank=True)
    EngineeringProductivity = models.CharField(max_length=5, blank=True)
    FrontendInfrastructure = models.CharField(max_length=5, blank=True)
    Growth = models.CharField(max_length=5, blank=True)
    Integrations = models.CharField(max_length=5, blank=True)
    Messaging = models.CharField(max_length=5, blank=True)
    Mobile = models.CharField(max_length=5, blank=True)
    ProductionSupport = models.CharField(max_length=5, blank=True)
    UberConference = models.CharField(max_length=5, blank=True)
    VoiceIntelligence = models.CharField(max_length=5, blank=True)
    Website = models.CharField(max_length=5, blank=True)
    Backlog = models.CharField(max_length=20, blank=True)
    Blocked = models.CharField(max_length=20, blank=True)
    CodeReview = models.CharField(max_length=20, blank=True)
    Closed = models.CharField(max_length=20, blank=True)
    InProgress = models.CharField(max_length=20, blank=True)
    NeedsTriage = models.CharField(max_length=20, blank=True)
    Open = models.CharField(max_length=20, blank=True)
    ReadyforTesting = models.CharField(max_length=20, blank=True)
    ReadyforProduction = models.CharField(max_length=20, blank=True)
    ToDo = models.CharField(max_length=20, blank=True)
    LastUpdate = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f" {self.id}: {self.One} {self.Two} {self.Three} {self.Four} {self.Five} {self.Six} \
                  {self.Seven}: {self.Eight} {self.Nine} {self.Ten} {self.Eleven} {self.Twelve} {self.Thirteen} \
                  {self.Fourteen}: {self.Fifteen} {self.Sixteen} {self.Seventeen} {self.Eighteen} {self.Nineteen} {self.Twenty} \
                  {self.Twentyone}: {self.Twentytwo} {self.Twentythree} {self.Twentyfour} {self.Twentyfive} {self.Twentysix} {self.Twentyseven} \
                  {self.Twentyeight}: {self.Twentynine} {self.Thirty} {self.Thirtyone} {self.AccountBilling} {self.Analytics} {self.BackendInfrastructure} \
                  {self.CallExperience}: {self.CallingFeatures} {self.ContactCenter} {self.CustomerAgentAssist} {self.DataInsights} {self.DeveloperPlatform} {self.Devices} \
                  {self.DialpadTalk}: {self.DigitalExperience} {self.EngineeringProductivity} {self.FrontendInfrastructure} {self.Growth} {self.Integrations} {self.Messaging} {self.Mobile} \
                  {self.ProductionSupport} {self.UberConference} {self.VoiceIntelligence} {self.Website} {self.Backlog} {self.Blocked} {self.CodeReview} {self.Closed} \
                  {self.InProgress} {self.NeedsTriage} {self.Open} {self.ReadyforTesting} {self.ReadyforProduction} {self.ToDo} {self.LastUpdate}"



class MOBExternal(models.Model):

    One = models.CharField(max_length=5, blank=True)
    Two = models.CharField(max_length=5, blank=True)
    Three = models.CharField(max_length=5, blank=True)
    Four = models.CharField(max_length=5, blank=True)
    Five = models.CharField(max_length=5, blank=True)
    Six = models.CharField(max_length=5, blank=True)
    Seven = models.CharField(max_length=5, blank=True)
    Eight = models.CharField(max_length=5, blank=True)
    Nine = models.CharField(max_length=5, blank=True)
    Ten = models.CharField(max_length=5, blank=True)
    Eleven = models.CharField(max_length=5, blank=True)
    Twelve = models.CharField(max_length=5, blank=True)
    Thirteen = models.CharField(max_length=5, blank=True)
    Fourteen = models.CharField(max_length=5, blank=True)
    Fifteen = models.CharField(max_length=5, blank=True)
    Sixteen = models.CharField(max_length=5, blank=True)
    Seventeen = models.CharField(max_length=5, blank=True)
    Eighteen = models.CharField(max_length=5, blank=True)
    Nineteen = models.CharField(max_length=5, blank=True)
    Twenty = models.CharField(max_length=5, blank=True)
    Twentyone = models.CharField(max_length=5, blank=True)
    Twentytwo = models.CharField(max_length=5, blank=True)
    Twentythree = models.CharField(max_length=5, blank=True)
    Twentyfour = models.CharField(max_length=5, blank=True)
    Twentyfive = models.CharField(max_length=5, blank=True)
    Twentysix = models.CharField(max_length=5, blank=True)
    Twentyseven = models.CharField(max_length=5, blank=True)
    Twentyeight = models.CharField(max_length=5, blank=True)
    Twentynine = models.CharField(max_length=5, blank=True)
    Thirty = models.CharField(max_length=5, blank=True)
    Thirtyone = models.CharField(max_length=5, blank=True)
    AccountBilling = models.CharField(max_length=5, blank=True)
    Analytics = models.CharField(max_length=5, blank=True)
    BackendInfrastructure = models.CharField(max_length=5, blank=True)
    CallExperience = models.CharField(max_length=5, blank=True)
    CallingFeatures = models.CharField(max_length=5, blank=True)
    ContactCenter = models.CharField(max_length=5, blank=True)
    CustomerAgentAssist = models.CharField(max_length=5, blank=True)
    DataInsights = models.CharField(max_length=5, blank=True)
    DeveloperPlatform = models.CharField(max_length=5, blank=True)
    Devices = models.CharField(max_length=5, blank=True)
    DialpadTalk = models.CharField(max_length=5, blank=True)
    DigitalExperience = models.CharField(max_length=5, blank=True)
    EngineeringProductivity = models.CharField(max_length=5, blank=True)
    FrontendInfrastructure = models.CharField(max_length=5, blank=True)
    Growth = models.CharField(max_length=5, blank=True)
    Integrations = models.CharField(max_length=5, blank=True)
    Messaging = models.CharField(max_length=5, blank=True)
    Mobile = models.CharField(max_length=5, blank=True)
    ProductionSupport = models.CharField(max_length=5, blank=True)
    UberConference = models.CharField(max_length=5, blank=True)
    VoiceIntelligence = models.CharField(max_length=5, blank=True)
    Website = models.CharField(max_length=5, blank=True)
    Backlog = models.CharField(max_length=20, blank=True)
    Blocked = models.CharField(max_length=20, blank=True)
    CodeReview = models.CharField(max_length=20, blank=True)
    Closed = models.CharField(max_length=20, blank=True)
    InProgress = models.CharField(max_length=20, blank=True)
    NeedsTriage = models.CharField(max_length=20, blank=True)
    Open = models.CharField(max_length=20, blank=True)
    ReadyforTesting = models.CharField(max_length=20, blank=True)
    ReadyforProduction = models.CharField(max_length=20, blank=True)
    ToDo = models.CharField(max_length=20, blank=True)
    LastUpdate = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f" {self.id}: {self.One} {self.Two} {self.Three} {self.Four} {self.Five} {self.Six} \
                  {self.Seven}: {self.Eight} {self.Nine} {self.Ten} {self.Eleven} {self.Twelve} {self.Thirteen} \
                  {self.Fourteen}: {self.Fifteen} {self.Sixteen} {self.Seventeen} {self.Eighteen} {self.Nineteen} {self.Twenty} \
                  {self.Twentyone}: {self.Twentytwo} {self.Twentythree} {self.Twentyfour} {self.Twentyfive} {self.Twentysix} {self.Twentyseven} \
                  {self.Twentyeight}: {self.Twentynine} {self.Thirty} {self.Thirtyone} {self.AccountBilling} {self.Analytics} {self.BackendInfrastructure} \
                  {self.CallExperience}: {self.CallingFeatures} {self.ContactCenter} {self.CustomerAgentAssist} {self.DataInsights} {self.DeveloperPlatform} {self.Devices} \
                  {self.DialpadTalk}: {self.DigitalExperience} {self.EngineeringProductivity} {self.FrontendInfrastructure} {self.Growth} {self.Integrations} {self.Messaging} {self.Mobile} \
                  {self.ProductionSupport} {self.UberConference} {self.VoiceIntelligence} {self.Website} {self.Backlog} {self.Blocked} {self.CodeReview} {self.Closed} \
                  {self.InProgress} {self.NeedsTriage} {self.Open} {self.ReadyforTesting} {self.ReadyforProduction} {self.ToDo} {self.LastUpdate}"


class ImpactAreas(models.Model):
    Area = models.CharField(max_length=30, blank=True)
    Number = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f" {self.id}: {self.Area} {self.Number}:"
    
class ImpactApplications(models.Model):
    Application = models.CharField(max_length=30, blank=True)
    Number = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f" {self.id}: {self.Application} {self.Number}:"

class EDACurrentMonth(models.Model):
    EDAType = models.CharField(max_length=30, blank=True)
    Number = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f" {self.id}: {self.EDAType} {self.Number}:"
    
class EDAPreviousMonth(models.Model):
    EDAType = models.CharField(max_length=30, blank=True)
    Number = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f" {self.id}: {self.EDAType} {self.Number}:"

class EDALearnings(models.Model):
    ActionItem = models.CharField(max_length=1000, blank=True)
    PreviousMonth = models.CharField(max_length=15, choices=month_options, blank=True)
    CurrentMonth = models.CharField(max_length=15, choices=month_options, blank=True)

    def __str__(self):
        return f"{self.id}: {self.ActionItem} {self.PreviousMonth} {self.CurrentMonth}"


class CFD(models.Model):
    CFDtotalJiras = models.CharField(max_length=150, blank=True)
    CFDtotalFixed = models.CharField(max_length=150, blank=True)
    CFDtotalMRT = models.CharField(max_length=150, blank=True)
    CFDtotalNotClosed = models.CharField(max_length=150, blank=True)
    CFDtotalCurrentFix = models.CharField(max_length=150, blank=True)
    CFDtotalNoise = models.CharField(max_length=150, blank=True)
    CFDtotalPriorityH = models.CharField(max_length=150, blank=True)
    CFDtotalPriorityM = models.CharField(max_length=150, blank=True)
    CFDtotalPriorityL = models.CharField(max_length=150, blank=True)
    CFDtotalPriorityU = models.CharField(max_length=150, blank=True)
    CFDtalkJiras = models.CharField(max_length=150, blank=True)
    CFDtalkFixed = models.CharField(max_length=150, blank=True)
    CFDtalkMRT = models.CharField(max_length=150, blank=True)
    CFDtalkNotClosed = models.CharField(max_length=150, blank=True)
    CFDtalkCurrentFix = models.CharField(max_length=150, blank=True)
    CFDtalkNoise = models.CharField(max_length=150, blank=True)
    CFDtalkPriorityH = models.CharField(max_length=150, blank=True)
    CFDtalkPriorityM = models.CharField(max_length=150, blank=True)
    CFDtalkPriorityL = models.CharField(max_length=150, blank=True)
    CFDtalkPriorityU = models.CharField(max_length=150, blank=True)
    CFDCCJiras = models.CharField(max_length=150, blank=True)
    CFDCCFixed = models.CharField(max_length=150, blank=True)
    CFDCCMRT = models.CharField(max_length=150, blank=True)
    CFDCCNotClosed = models.CharField(max_length=150, blank=True)
    CFDCCCurrentFix = models.CharField(max_length=150, blank=True)
    CFDCCNoise = models.CharField(max_length=150, blank=True)
    CFDCCPriorityH = models.CharField(max_length=150, blank=True)
    CFDCCPriorityM = models.CharField(max_length=150, blank=True)
    CFDCCPriorityL = models.CharField(max_length=150, blank=True)
    CFDCCPriorityU = models.CharField(max_length=150, blank=True)
    CFDINTJiras = models.CharField(max_length=150, blank=True)
    CFDINTFixed = models.CharField(max_length=150, blank=True)
    CFDINTMRT = models.CharField(max_length=150, blank=True)
    CFDINTNotClosed = models.CharField(max_length=150, blank=True)
    CFDINTCurrentFix = models.CharField(max_length=150, blank=True)
    CFDINTNoise = models.CharField(max_length=150, blank=True)
    CFDLastUpdate = models.CharField(max_length=60, blank=True)
    CFDINTPriorityH = models.CharField(max_length=150, blank=True)
    CFDINTPriorityM = models.CharField(max_length=150, blank=True)
    CFDINTPriorityL = models.CharField(max_length=150, blank=True)
    CFDINTPriorityU = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.id}: {self.CFDtotalJiras} {self.CFDtotalFixed} {self.CFDtotalMRT} {self.CFDtotalNotClosed} {self.CFDtotalCurrentFix} {self.CFDtotalNoise} {self.CFDtotalPriorityH} {self.CFDtotalPriorityM} {self.CFDtotalPriorityL} {self.CFDtotalPriorityU}\
               {self.CFDtalkJiras} {self.CFDtalkFixed} {self.CFDtalkMRT} {self.CFDtalkNotClosed} {self.CFDtalkCurrentFix} {self.CFDtalkNoise} {self.CFDtalkPriorityH} {self.CFDtalkPriorityM} {self.CFDtalkPriorityL} {self.CFDtalkPriorityU}\
               {self.CFDCCJiras} {self.CFDCCFixed} {self.CFDCCMRT} {self.CFDCCNotClosed} {self.CFDCCCurrentFix} {self.CFDCCNoise} {self.CFDCCPriorityH} {self.CFDCCPriorityM} {self.CFDCCPriorityL} {self.CFDCCPriorityU}\
               {self.CFDINTJiras} {self.CFDINTFixed} {self.CFDINTMRT} {self.CFDINTNotClosed} {self.CFDINTCurrentFix} {self.CFDINTNoise} {self.CFDINTPriorityH} {self.CFDINTPriorityM} {self.CFDINTPriorityL} {self.CFDINTPriorityU} {self.CFDLastUpdate}"


class IFD(models.Model):
    IFDtotalJiras = models.CharField(max_length=150, blank=True)
    IFDtotalFixed = models.CharField(max_length=150, blank=True)
    IFDtotalMRT = models.CharField(max_length=150, blank=True)
    IFDtotalNotClosed = models.CharField(max_length=150, blank=True)
    IFDtotalCurrentFix = models.CharField(max_length=150, blank=True)
    IFDtotalNoise = models.CharField(max_length=150, blank=True)
    IFDtalkJiras = models.CharField(max_length=150, blank=True)
    IFDtalkFixed = models.CharField(max_length=150, blank=True)
    IFDtalkMRT = models.CharField(max_length=150, blank=True)
    IFDtalkNotClosed = models.CharField(max_length=150, blank=True)
    IFDtalkCurrentFix = models.CharField(max_length=150, blank=True)
    IFDtalkNoise = models.CharField(max_length=150, blank=True)
    IFDCCJiras = models.CharField(max_length=150, blank=True)
    IFDCCFixed = models.CharField(max_length=150, blank=True)
    IFDCCMRT = models.CharField(max_length=150, blank=True)
    IFDCCNotClosed = models.CharField(max_length=150, blank=True)
    IFDCCCurrentFix = models.CharField(max_length=150, blank=True)
    IFDCCNoise = models.CharField(max_length=150, blank=True)
    IFDINTJiras = models.CharField(max_length=150, blank=True)
    IFDINTFixed = models.CharField(max_length=150, blank=True)
    IFDINTMRT = models.CharField(max_length=150, blank=True)
    IFDINTNotClosed = models.CharField(max_length=150, blank=True)
    IFDINTCurrentFix = models.CharField(max_length=150, blank=True)
    IFDINTNoise = models.CharField(max_length=150, blank=True)
    IFDLastUpdate = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f"{self.id}: {self.IFDtotalJiras} {self.IFDtotalFixed} {self.IFDtotalMRT} {self.IFDtotalNotClosed} {self.IFDtotalCurrentFix} {self.IFDtotalNoise} \
               {self.IFDtalkJiras} {self.IFDtalkFixed} {self.IFDtalkMRT} {self.IFDtalkNotClosed} {self.IFDtalkCurrentFix} {self.IFDtalkNoise} \
               {self.IFDCCJiras} {self.IFDCCFixed} {self.IFDCCMRT} {self.IFDCCNotClosed} {self.IFDCCCurrentFix} {self.IFDCCNoise} \
               {self.IFDINTJiras} {self.IFDINTFixed} {self.IFDINTMRT} {self.IFDINTNotClosed} {self.IFDINTCurrentFix} {self.IFDINTNoise} {self.IFDLastUpdate}"


class CFDDPM(models.Model):
    DPMCFDtotalJiras = models.CharField(max_length=150, blank=True)
    DPMCFDtotalFixed = models.CharField(max_length=150, blank=True)
    DPMCFDtotalMRT = models.CharField(max_length=150, blank=True)
    DPMCFDtotalNotClosed = models.CharField(max_length=150, blank=True)
    DPMCFDtotalCurrentFix = models.CharField(max_length=150, blank=True)
    DPMCFDtotalNoise = models.CharField(max_length=150, blank=True)
    DPMCFDtotalPriorityH = models.CharField(max_length=150, blank=True)
    DPMCFDtotalPriorityM = models.CharField(max_length=150, blank=True)
    DPMCFDtotalPriorityL = models.CharField(max_length=150, blank=True)
    DPMCFDtotalPriorityU = models.CharField(max_length=150, blank=True)
    DPMCFDLastUpdate = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f"{self.id}: {self.DPMCFDtotalJiras} {self.DPMCFDtotalFixed} {self.DPMCFDtotalMRT} {self.DPMCFDtotalNotClosed} {self.DPMCFDtotalCurrentFix} {self.DPMCFDtotalNoise} {self.DPMCFDtotalPriorityH} {self.DPMCFDtotalPriorityM} {self.DPMCFDtotalPriorityL} {self.DPMCFDtotalPriorityU} {self.DPMCFDLastUpdate}"


class CFDMOB(models.Model):
    MOBCFDtotalJiras = models.CharField(max_length=150, blank=True)
    MOBCFDtotalFixed = models.CharField(max_length=150, blank=True)
    MOBCFDtotalMRT = models.CharField(max_length=150, blank=True)
    MOBCFDtotalNotClosed = models.CharField(max_length=150, blank=True)
    MOBCFDtotalCurrentFix = models.CharField(max_length=150, blank=True)
    MOBCFDtotalNoise = models.CharField(max_length=150, blank=True)
    MOBCFDtotalPriorityH = models.CharField(max_length=150, blank=True)
    MOBCFDtotalPriorityM = models.CharField(max_length=150, blank=True)
    MOBCFDtotalPriorityL = models.CharField(max_length=150, blank=True)
    MOBCFDtotalPriorityU = models.CharField(max_length=150, blank=True)
    MOBCFDLastUpdate = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f"{self.id}: {self.MOBCFDtotalJiras} {self.MOBCFDtotalFixed} {self.MOBCFDtotalMRT} {self.MOBCFDtotalNotClosed} {self.MOBCFDtotalCurrentFix} {self.MOBCFDtotalNoise} {self.MOBCFDtotalPriorityH} {self.MOBCFDtotalPriorityM} {self.MOBCFDtotalPriorityL} {self.MOBCFDtotalPriorityU} {self.MOBCFDLastUpdate}"
